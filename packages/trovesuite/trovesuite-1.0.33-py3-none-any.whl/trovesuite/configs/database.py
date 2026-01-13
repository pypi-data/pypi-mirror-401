"""
Database configuration and connection management

FIXED VERSION - Removed pool reinitialization during runtime to prevent "unkeyed connection" errors.
Key changes:
- Pool created once at startup, never recreated during runtime
- Removed connection validation queries that consume pool connections
- Increased default pool size to 2 (safe for Azure Basic tier)
- Simplified get_db_connection() - let pool.getconn() block naturally
- Removed _recover_connection_pool() and _is_pool_valid() runtime checks

NOTE: Database initialization is NOT automatic for package version.
You must call initialize_database() explicitly in your application startup.
Example in FastAPI:
    @app.on_event("startup")
    async def startup_event():
        initialize_database()
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

# Database connection pool - created once at startup, never replaced during runtime
_connection_pool: Optional[psycopg2.pool.ThreadedConnectionPool] = None
_initialization_lock = threading.Lock()


class DatabaseConfig:
    """Database configuration and connection management"""

    def __init__(self):
        import os
        self.settings = db_settings
        self.database_url = self.settings.database_url
        # Safe pool size for Azure Basic tier (B_Standard_B1ms)
        # With 2 workers and pool_size=5: 2 × 5 = 10 connections (safe, well under 50 limit)
        # Increased from 2 to 5 to handle concurrent auth + business logic better
        # Can be overridden with DB_POOL_SIZE environment variable
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "5"))

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
        """Create a connection pool for psycopg2"""
        try:
            import os
            dsn = os.getenv("DATABASE_URL", "") or str(self.database_url or "")
            is_azure = "database.azure.com" in dsn.lower()
            pool_size = self.pool_size
            
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
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ["connection", "slot", "limit", "exhausted", "too many"]):
                logger.error("⚠️  Database connection limit reached!")
                logger.error("   Possible causes:")
                logger.error("   1. Too many connections from multiple replicas/workers")
                logger.error("   2. Pool size too high (DB_POOL_SIZE environment variable)")
                logger.error("   3. Too many Gunicorn workers (GUNICORN_WORKERS environment variable)")
                logger.error("   4. Connections not being properly returned to pool")
                logger.error("   Solutions:")
                logger.error("   - Set DB_POOL_SIZE=2 (current default)")
                logger.error("   - Reduce GUNICORN_WORKERS (default: 2)")
                logger.error("   - Consider using PgBouncer for connection pooling")
                logger.error("   - Upgrade to a higher PostgreSQL tier if needed")
            logger.error(f"Failed to create database connection pool: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to create database connection pool: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """Test database connection (only used at startup)"""
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
    """
    Initialize database connections and pool.
    This should ONLY be called at application startup.
    Pool is created once and never recreated during runtime.
    
    NOTE: For package version, this must be called explicitly in application startup.
    """
    global _connection_pool
    
    with _initialization_lock:
        # If pool already exists, don't recreate it
        if _connection_pool is not None:
            logger.warning("Database pool already initialized, skipping reinitialization")
            return
        
        try:
            # Test connection first (only at startup)
            if not db_config.test_connection():
                raise Exception("Database connection test failed")

            # Create connection pool (only once at startup)
            _connection_pool = db_config.create_connection_pool()
            
            # Verify pool was created successfully
            if _connection_pool is None:
                raise Exception("Connection pool creation returned None")

            logger.info("✅ Database initialization completed successfully")

        except Exception as e:
            logger.error(f"❌ Database initialization failed: {str(e)}")
            _connection_pool = None  # Ensure pool is None on failure
            raise


def get_connection_pool() -> psycopg2.pool.ThreadedConnectionPool:
    """
    Get the database connection pool.
    Pool must be initialized at startup. This function will raise if pool is None.
    """
    global _connection_pool
    
    if _connection_pool is None:
        error_msg = (
            "Database connection pool is not initialized. "
            "Please ensure initialize_database() was called at application startup."
        )
        logger.error(error_msg)
        raise Exception(error_msg)
    
    return _connection_pool


@contextmanager
def get_db_connection():
    """
    Get a database connection from the pool (context manager).
    
    This is simplified - we let pool.getconn() block naturally.
    No retries, no validation queries, no pool recovery.
    """
    pool = get_connection_pool()
    conn = None
    try:
        # Get connection from pool - this will block if pool is exhausted
        # That's the correct behavior - let backpressure happen naturally
        conn = pool.getconn()
        logger.debug("Database connection acquired from pool")
        yield conn
    except Exception as e:
        # If connection exists and isn't closed, rollback transaction
        if conn and not conn.closed:
            try:
                conn.rollback()
            except Exception as rollback_error:
                logger.warning(f"Could not rollback transaction: {str(rollback_error)}")
        # Re-raise the exception - don't retry here
        raise
    finally:
        # Always return connection to pool
        if conn:
            try:
                if conn.closed:
                    # If connection is closed, tell pool to close it instead of returning
                    pool.putconn(conn, close=True)
                else:
                    # Return connection to pool normally
                    pool.putconn(conn)
                logger.debug("Database connection returned to pool")
            except Exception as put_error:
                # Log error but don't fail - connection will be cleaned up by pool
                logger.error(f"Error returning connection to pool: {str(put_error)}")
                # Try to close connection manually as last resort
                try:
                    if not conn.closed:
                        conn.close()
                except Exception:
                    pass


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
        # Use get_db_connection() instead of directly accessing pool
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
        """
        Perform database health check.
        Health checks are allowed to fail - they don't attempt to repair the pool.
        """
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


# NOTE: Database initialization is NOT automatic for package version
# You must call initialize_database() explicitly in your application startup
# Example in FastAPI:
#   @app.on_event("startup")
#   async def startup_event():
#       initialize_database()
