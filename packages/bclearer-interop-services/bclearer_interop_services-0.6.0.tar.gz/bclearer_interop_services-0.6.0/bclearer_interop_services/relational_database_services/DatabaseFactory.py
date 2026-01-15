from bclearer_interop_services.relational_database_services.postgresql.PostgresqlFacade import (
    PostgresqlFacade,
)
from bclearer_interop_services.relational_database_services.sqlite.SqliteFacade import (
    SqliteFacade,
)


# Factory class to get the correct database implementation
class DatabaseFactory:
    @staticmethod
    def get_database(
        db_type,
        host=None,
        database=None,
        user=None,
        password=None,
        port=None,
    ):
        """Create a database facade instance.

        Args:
            db_type: Database type ("postgresql" or "sqlite")
            host: Database host (PostgreSQL only)
            database: Database name (PostgreSQL) or file path (SQLite)
            user: Username (PostgreSQL only)
            password: Password (PostgreSQL only)
            port: Port number (PostgreSQL only)

        Returns:
            DatabaseFacade instance

        Examples:
            # PostgreSQL
            db = DatabaseFactory.get_database(
                "postgresql",
                host="localhost",
                database="mydb",
                user="admin",
                password="secret",
                port=5432
            )

            # SQLite
            db = DatabaseFactory.get_database(
                "sqlite",
                database="/data/mydb.db"  # Only database parameter needed
            )
        """
        if db_type == "postgresql":
            return PostgresqlFacade(
                host,
                database,
                user,
                password,
                port=port,
            )
        elif db_type == "sqlite":
            return SqliteFacade(
                host=host,  # Ignored but accepted for API consistency
                database=database,  # Used as file path
                user=user,  # Ignored
                password=password,  # Ignored
                port=port,  # Ignored
            )
        else:
            raise ValueError(
                f"Unsupported database type: {db_type}. "
                f"Supported types: 'postgresql', 'sqlite'"
            )
