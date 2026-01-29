import time
import pymysql
from urllib.parse import quote
from contextlib import contextmanager

from sqlalchemy import create_engine, text, bindparam
from shared_kernel.constants.constants import get_constant
from sqlalchemy.orm import sessionmaker
from shared_kernel.dataclasses.warehouse_configs import MySQLConfig
from shared_kernel.interfaces.warehouse_connection import DataWarehouseConnection
from sqlalchemy.exc import OperationalError, ProgrammingError, InterfaceError

from shared_kernel.exceptions.http_exceptions import BadRequest
from shared_kernel.config import Config
from shared_kernel.logger import Logger

config = Config()
logger = Logger(config.get("APP_NAME"))


class MySQLWarehouseConnection(DataWarehouseConnection):

    SYSTEM_SCHEMAS = ("information_schema", "mysql",
                      "performance_schema", "sys")
    LIST_SCHEMAS_QUERY = """
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name NOT IN :system_schemas 
        ORDER BY schema_name
    """

    def __init__(self, source_config: MySQLConfig):
        super().__init__(source_config)
        self._engine = None
        self._session = None
        self._mysql_config = source_config

    def _create_connection_with_retry(self, retries: int = 3, delay: int = 5):
        """Try to establish a connection with retry mechanism."""
        for attempt in range(retries):
            try:
                try:
                    cfg = self._mysql_config
                    logger.debug(
                        f"MySQL connection configuration: {cfg.__dict__}")

                    host = cfg.host
                    port = int(cfg.port)
                    database = cfg.database
                    username = cfg.username
                    password = quote(cfg.password)

                    connection_string = get_constant(
                        "mysql", "CONNECTION_STRING"
                    ).format(username, password, host, port, database)

                    # pymysql conversion for BIT representation to boolean to resolve JSON serialization error
                    connection_args = {
                        'conv': {
                            pymysql.FIELD_TYPE.BIT: lambda data: data == b'\x01'
                        }
                    }
                    self._engine = create_engine(
                        connection_string, connect_args=connection_args)
                    self._session = sessionmaker(bind=self._engine)()

                    # Disabling connection validation for performance optimization
                    # if not self.is_valid_connection():
                    #     raise BadRequest("Connection validation failed")
                    return

                except (OperationalError, ProgrammingError, InterfaceError) as e:
                    raise BadRequest(
                        f"Connection to warehouse failed: {str(e)}")
            except BadRequest as e:
                if attempt == retries - 1:
                    raise

            except Exception as e:
                if attempt == retries - 1:
                    raise BadRequest(
                        f"Failed to connect after {retries} attempts due to {str(e)}"
                    ) from e

                time.sleep(delay)
                self.close_connection()

    @contextmanager
    def get_connection(self, retries: int = 3, delay: int = 5):
        """Context manager for database connections with retry mechanism"""
        if not (self._session and self.is_valid_connection()):
            self._create_connection_with_retry(retries, delay)
        try:
            yield self._session
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        finally:
            self.close_connection()

    def test_connection(self):

        try:
            cfg = self._mysql_config
            logger.debug(f"MySQL connection configuration: {cfg.__dict__}")

            host = cfg.host
            port = int(cfg.port)
            database = cfg.database
            username = cfg.username
            password = quote(cfg.password)

            connection_string = get_constant(
                "mysql", "CONNECTION_STRING"
            ).format(username, password, host, port, database)

            # pymysql conversion for BIT representation to boolean to resolve JSON serialization error
            connection_args = {
                'conv': {
                    pymysql.FIELD_TYPE.BIT: lambda data: data == b'\x01'
                }
            }
            engine = create_engine(
                connection_string, connect_args=connection_args)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True

        except OperationalError as e:
            if "password authentication failed" in str(e).lower() or "authentication failed" in str(e).lower():
                raise ValueError("Invalid username or password")
            raise ConnectionError(f" Database error: {str(e)}")
        except InterfaceError as e:
            raise ConnectionError("Cannot connect to database server")
        except Exception as e:
            raise ConnectionError(f"Connection failed: {str(e)}")

    def is_valid_connection(self) -> bool:
        """Validate connection with a simple query."""
        try:
            if self._session is None:
                return False

            result = self._session.execute(
                text("SELECT USER(), DATABASE(), VERSION()")
            )
            user, db, version = result.fetchone()
            logger.debug(
                f"Connected as {user} to {db}, version: {version}"
            )
            return True
        except (OperationalError, ProgrammingError, InterfaceError) as e:
            raise e
        except Exception as e:
            raise Exception(
                f"Connection validation failed."
            )

    def close_connection(self):
        """Safely close database connection"""
        try:
            if self._session:
                self._session.close()
            if self._engine:
                self._engine.dispose()
        except Exception as e:
            logger.error(
                f"Error closing MySQL connection: {str(e)}",
                exc_info=True,
            )
        finally:
            self._session = None
            self._engine = None
