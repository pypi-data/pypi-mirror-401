"""
Database configuration and connection management
"""
from contextlib import contextmanager
from typing import Generator, Optional
import psycopg2
import psycopg2.pool
from psycopg2.extras import RealDictCursor
import threading
from .settings import db_settings
from .logging import get_logger

logger = get_logger("database")

# Database connection pool
_connection_pool: Optional[psycopg2.pool.ThreadedConnectionPool] = None
_initialization_lock = threading.Lock()


class DatabaseConfig:
    """Database configuration and connection management"""

    def __init__(self):
        import os
        self.settings = db_settings
        self.database_url = self.settings.database_url
        # CRITICAL: Azure PostgreSQL B_Standard_B1ms has very limited connections (~50 max, practical limit ~30-40)
        # Default pool size is set to 1 to avoid connection exhaustion with multiple workers/replicas
        # Formula: connections = pool_size × workers × replicas
        # Example: 1 pool × 4 workers × 2 replicas = 8 connections (safe)
        # With old default (5): 5 × 4 × 2 = 40 connections (exceeds limit!)
        # Can be overridden with DB_POOL_SIZE environment variable
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "1"))

    def get_connection_params(self) -> dict:
        """Get database connection parameters"""
        if self.settings.DATABASE_URL:
            # Use full DATABASE_URL if available
            return {
                "dsn": self.settings.DATABASE_URL,
                "cursor_factory": RealDictCursor,
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
                "connect_timeout": 30  # Increased timeout for Azure PostgreSQL
            }

        # fallback to individual DB_* variables
        return {
            "host": self.settings.DB_HOST,
            "port": self.settings.DB_PORT,
            "database": self.settings.DB_NAME,
            "user": self.settings.DB_USER,
            "password": self.settings.DB_PASSWORD,
            "cursor_factory": RealDictCursor,
            "application_name": f"{self.settings.APP_NAME}_{self.settings.ENVIRONMENT}",
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
            "connect_timeout": 10
        }

    def create_connection_pool(self) -> psycopg2.pool.ThreadedConnectionPool:
        """Create a connection pool for psycopg2
        
        Note: For Azure PostgreSQL B_Standard_B1ms, keep pool_size ≤ 1 per worker
        to avoid connection exhaustion. Consider using PgBouncer for higher concurrency.
        """
        try:
            # For Azure PostgreSQL, use minimum pool size to avoid connection exhaustion
            # Multiple replicas/workers can quickly exhaust database connections on Basic tier
            import os
            dsn = os.getenv("DATABASE_URL", "") or str(self.database_url or "")
            is_azure = "database.azure.com" in dsn.lower()
            
            # Ensure pool size is appropriate for Azure Basic tier
            pool_size = self.pool_size
            if is_azure and pool_size > 2:
                logger.warning(
                    f"⚠️  Pool size {pool_size} may be too high for Azure Basic tier. "
                    f"Recommended: 1-2 connections per worker. "
                    f"Set DB_POOL_SIZE=1 to avoid connection exhaustion."
                )
            
            pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=pool_size,
                **self.get_connection_params()
            )
            logger.info(
                f"Database connection pool created with {pool_size} connections "
                f"(Azure: {is_azure}, DB_POOL_SIZE: {self.pool_size})"
            )
            return pool
        except psycopg2.OperationalError as e:
            # Check if it's a connection limit error
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ["connection", "slot", "limit", "exhausted", "too many"]):
                logger.error("⚠️  Database connection limit reached!")
                logger.error("   Possible causes:")
                logger.error("   1. Too many connections from multiple replicas/workers")
                logger.error("   2. Pool size too high (DB_POOL_SIZE environment variable)")
                logger.error("   3. Too many Gunicorn workers (GUNICORN_WORKERS environment variable)")
                logger.error("   4. Connections not being properly returned to pool")
                logger.error("   Solutions:")
                logger.error("   - Set DB_POOL_SIZE=1 (recommended for Azure Basic tier)")
                logger.error("   - Reduce GUNICORN_WORKERS (default: 4)")
                logger.error("   - Consider using PgBouncer for connection pooling")
                logger.error("   - Upgrade to a higher PostgreSQL tier if needed")
            logger.error(f"Failed to create database connection pool: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to create database connection pool: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with psycopg2.connect(**self.get_connection_params()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    if result:
                        logger.info("Database connection test successful")
                        return True
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False
        return False


# Global database configuration
db_config = DatabaseConfig()


def initialize_database():
    """Initialize database connections and pool"""
    global _connection_pool
    
    # Close existing pool if it exists (cleanup before reinitializing)
    if _connection_pool is not None:
        try:
            _connection_pool.closeall()
            logger.info("Closed existing connection pool before reinitialization")
        except Exception as e:
            logger.warning(f"Error closing existing pool: {str(e)}")
        _connection_pool = None

    try:
        # Test connection first
        if not db_config.test_connection():
            raise Exception("Database connection test failed")

        # Create connection pool
        _connection_pool = db_config.create_connection_pool()
        
        # Verify pool was created successfully
        if _connection_pool is None:
            raise Exception("Connection pool creation returned None")

        logger.info("✅ Database initialization completed successfully")

    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        _connection_pool = None  # Ensure pool is None on failure
        raise


def _is_pool_valid(pool) -> bool:
    """Check if the connection pool is valid and usable"""
    if pool is None:
        return False
    try:
        # ThreadedConnectionPool doesn't expose a direct "closed" attribute
        # Check if pool has the necessary internal structures
        if not hasattr(pool, '_pool'):
            return False
        if pool._pool is None:
            return False
        # Additional check: verify pool has connection parameters
        if not hasattr(pool, '_kwargs'):
            return False
        return True
    except (AttributeError, Exception) as e:
        logger.debug(f"Pool validation check: {str(e)}")
        return False


def _recover_connection_pool() -> bool:
    """Attempt to recover the connection pool with retry logic"""
    global _connection_pool, _initialization_lock
    import time
    
    with _initialization_lock:
        # Double-check after acquiring lock
        if _connection_pool is not None and _is_pool_valid(_connection_pool):
            return True
        
        # Close invalid pool if it exists
        if _connection_pool is not None:
            try:
                _connection_pool.closeall()
                logger.info("Closed invalid connection pool")
            except Exception as e:
                logger.warning(f"Error closing invalid pool: {str(e)}")
            _connection_pool = None
        
        # Retry with exponential backoff
        max_retries = 3
        base_delay = 1  # Start with 1 second
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.warning(f"Attempting to reinitialize connection pool (attempt {attempt}/{max_retries})...")
                initialize_database()
                
                if _connection_pool is not None and _is_pool_valid(_connection_pool):
                    logger.info(f"✅ Connection pool reinitialized successfully (attempt {attempt})")
                    return True
                else:
                    logger.warning(f"Pool initialized but validation failed (attempt {attempt})")
                    
            except Exception as e:
                logger.error(f"Pool reinitialization attempt {attempt} failed: {str(e)}")
                if attempt < max_retries:
                    delay = base_delay * (2 ** (attempt - 1))  # Exponential backoff: 1s, 2s, 4s
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        
        logger.error("❌ Failed to reinitialize connection pool after all retries")
        return False


def get_connection_pool() -> psycopg2.pool.ThreadedConnectionPool:
    """Get the database connection pool, with automatic reinitialization if needed"""
    global _connection_pool
    
    # Fast path: pool exists and is valid
    if _connection_pool is not None and _is_pool_valid(_connection_pool):
        return _connection_pool
    
    # Pool is None or invalid, attempt recovery
    if not _recover_connection_pool():
        error_msg = (
            "Database connection pool is unavailable. This usually means:\n"
            "1. Database server is unreachable or down\n"
            "2. Network connectivity issues\n"
            "3. Database credentials are incorrect\n"
            "4. Connection pool exhausted or closed\n"
            "5. Database initialization failed\n"
            "Please check the startup logs and database status."
        )
        logger.error(error_msg)
        raise Exception(error_msg)
    
    if _connection_pool is None:
        error_msg = "Connection pool recovery completed but pool is still None"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    return _connection_pool


def _validate_connection(conn) -> bool:
    """Validate if a connection is still alive"""
    try:
        # Check if connection is closed first
        if conn.closed:
            return False
        
        # Test if connection is alive with a simple query
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True
    except (psycopg2.OperationalError, psycopg2.InterfaceError, psycopg2.DatabaseError) as e:
        logger.warning(f"Connection validation failed: {str(e)}")
        return False
    except Exception as e:
        logger.warning(f"Unexpected error during connection validation: {str(e)}")
        return False


@contextmanager
def get_db_connection():
    """Get a database connection from the pool (context manager)"""
    pool = get_connection_pool()
    conn = None
    try:
        conn = pool.getconn()

        # Validate connection before using it
        if not _validate_connection(conn):
            logger.warning("Stale connection detected, getting new connection")
            pool.putconn(conn, close=True)
            conn = pool.getconn()

        logger.debug("Database connection acquired from pool")
        yield conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        if conn:
            try:
                # Only rollback if connection is still open
                if not conn.closed:
                    conn.rollback()
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as rollback_error:
                logger.warning(f"Could not rollback closed connection: {str(rollback_error)}")
        raise
    finally:
        if conn:
            try:
                # If connection is broken, close it instead of returning to pool
                if conn.closed:
                    pool.putconn(conn, close=True)
                else:
                    pool.putconn(conn)
                logger.debug("Database connection returned to pool")
            except Exception as put_error:
                logger.error(f"Error returning connection to pool: {str(put_error)}")


@contextmanager
def get_db_cursor():
    """Get a database cursor (context manager)"""
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if not conn.closed:
                conn.commit()
        except Exception as e:
            if not conn.closed:
                try:
                    conn.rollback()
                except (psycopg2.OperationalError, psycopg2.InterfaceError) as rollback_error:
                    logger.warning(f"Could not rollback transaction on closed connection: {str(rollback_error)}")
            logger.error(f"Database cursor error: {str(e)}")
            raise
        finally:
            try:
                cursor.close()
            except Exception as close_error:
                logger.warning(f"Error closing cursor: {str(close_error)}")


class DatabaseManager:
    """Database manager for common operations"""

    @staticmethod
    def execute_query(query: str, params: tuple = None) -> list:
        """Execute a SELECT query and return results"""
        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    def execute_update(query: str, params: tuple = None) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

    @staticmethod
    def execute_scalar(query: str, params: tuple = None):
        """Execute a query and return a single value"""
        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            if result:
                # Handle RealDictRow (dictionary-like) result
                if hasattr(result, 'get'):
                    # For RealDictRow, get the first value
                    return list(result.values())[0] if result else None
                else:
                    # Handle tuple result
                    return result[0] if len(result) > 0 else None
            return None

    @staticmethod
    @contextmanager
    def transaction():
        """
        Context manager for database transactions.
        Wraps multiple operations in a single transaction.

        Usage:
            with DatabaseManager.transaction() as cursor:
                cursor.execute("INSERT INTO table1 ...")
                cursor.execute("INSERT INTO table2 ...")
                # Auto-commits on success, auto-rollbacks on exception
        """
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
                if not conn.closed:
                    conn.commit()
                    logger.debug("Transaction committed successfully")
            except Exception as e:
                if not conn.closed:
                    try:
                        conn.rollback()
                        logger.warning(f"Transaction rolled back due to error: {str(e)}")
                    except (psycopg2.OperationalError, psycopg2.InterfaceError) as rollback_error:
                        logger.error(f"Could not rollback transaction: {str(rollback_error)}")
                raise
            finally:
                try:
                    cursor.close()
                except Exception as close_error:
                    logger.warning(f"Error closing transaction cursor: {str(close_error)}")

    @staticmethod
    def health_check() -> dict:
        """Perform database health check"""
        try:
            with get_db_cursor() as cursor:
                cursor.execute("SELECT version(), current_database(), current_user")
                result = cursor.fetchone()

                if result:
                    # Handle RealDictRow (dictionary-like) result
                    if hasattr(result, 'get'):
                        return {
                            "status": "healthy",
                            "database": result.get('current_database', 'unknown'),
                            "user": result.get('current_user', 'unknown'),
                            "version": result.get('version', 'unknown')
                        }
                    else:
                        # Handle tuple result
                        return {
                            "status": "healthy",
                            "database": result[1] if len(result) > 1 else "unknown",
                            "user": result[2] if len(result) > 2 else "unknown",
                            "version": result[0] if len(result) > 0 else "unknown"
                        }
                else:
                    return {
                        "status": "unhealthy",
                        "error": "No result from database query"
                    }
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# NOTE: Database initialization is NOT automatic
# You must call initialize_database() explicitly in your application startup
# Example in FastAPI:
#   @app.on_event("startup")
#   async def startup_event():
#       initialize_database()