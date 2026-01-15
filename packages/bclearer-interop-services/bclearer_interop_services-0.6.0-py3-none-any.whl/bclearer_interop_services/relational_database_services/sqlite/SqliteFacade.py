import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from bclearer_interop_services.relational_database_services.RelationaDatabaseFacade import (
    DatabaseFacade,
)


class SqliteFacade(DatabaseFacade):
    """SQLite implementation of DatabaseFacade.

    Note: SQLite doesn't use host/port/user/password, but we accept them
    for API compatibility. Only 'database' parameter is used as the file path.
    """

    def __init__(
        self,
        host: str = None,  # Ignored for SQLite
        database: str = None,  # Used as file path
        user: str = None,  # Ignored for SQLite
        password: str = None,  # Ignored for SQLite
        port: int = None,  # Ignored for SQLite
    ):
        # For compatibility with parent class
        super().__init__(host, database, user, password, port)

        # SQLite uses database parameter as file path
        self.database_path = database
        if not self.database_path:
            raise ValueError("database parameter must be provided (used as file path)")

    def connect(self):
        """Establish connection to SQLite database."""
        # Ensure parent directory exists
        db_path = Path(self.database_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False,  # Allow multi-threaded access
        )
        # Enable foreign keys (disabled by default in SQLite)
        self.connection.execute("PRAGMA foreign_keys = ON")
        # Use Row factory for dict-like access
        self.connection.row_factory = sqlite3.Row

    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(
        self,
        query: str,
        params: Optional[Union[tuple, dict, list]] = None,
    ):
        """Execute a query without returning results.

        Args:
            query: SQL query (use ? placeholders)
            params: Query parameters (tuple, dict, or list)
        """
        if not self.connection:
            raise RuntimeError("Not connected. Call connect() first.")

        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
        finally:
            cursor.close()

    def fetch_results(
        self,
        query: str,
        params: Optional[Union[tuple, dict, list]] = None,
    ) -> pd.DataFrame:
        """Execute a query and return results as a DataFrame.

        Args:
            query: SQL query (use ? placeholders)
            params: Query parameters (tuple, dict, or list)

        Returns:
            DataFrame containing query results
        """
        if not self.connection:
            raise RuntimeError("Not connected. Call connect() first.")

        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            results = cursor.fetchall()

            return pd.DataFrame(results, columns=columns)
        finally:
            cursor.close()

    def store_dataframe(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
    ):
        """Store a DataFrame in a table.

        Creates table if it doesn't exist, validates schema if it does.

        Args:
            dataframe: DataFrame to store
            table_name: Name of the table
        """
        if not self.connection:
            raise RuntimeError("Not connected. Call connect() first.")

        cursor = self.connection.cursor()
        try:
            # Check if table exists
            cursor.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type='table' AND name=?
                """,
                (table_name,),
            )

            table_exists = cursor.fetchone() is not None

            if table_exists:
                # Validate schema
                cursor.execute(f"PRAGMA table_info({table_name})")
                db_schema = cursor.fetchall()
                db_columns = {row[1] for row in db_schema}  # row[1] is column name
                df_columns = set(dataframe.columns)

                if db_columns != df_columns:
                    raise ValueError(
                        f"Schema mismatch: DB columns {db_columns} "
                        f"vs DataFrame columns {df_columns}"
                    )

                # Insert data
                placeholders = ", ".join(["?"] * len(dataframe.columns))
                insert_query = (
                    f"INSERT INTO {table_name} "
                    f"({', '.join(dataframe.columns)}) "
                    f"VALUES ({placeholders})"
                )

                for row in dataframe.itertuples(index=False, name=None):
                    cursor.execute(insert_query, row)
            else:
                # Create table and insert data
                col_defs = ", ".join(
                    [
                        f"{col} {self._map_dtype(dtype)}"
                        for col, dtype in zip(dataframe.columns, dataframe.dtypes)
                    ]
                )
                cursor.execute(f"CREATE TABLE {table_name} ({col_defs})")

                # Insert data
                placeholders = ", ".join(["?"] * len(dataframe.columns))
                insert_query = (
                    f"INSERT INTO {table_name} "
                    f"({', '.join(dataframe.columns)}) "
                    f"VALUES ({placeholders})"
                )

                for row in dataframe.itertuples(index=False, name=None):
                    cursor.execute(insert_query, row)

            self.connection.commit()
        finally:
            cursor.close()

    def _map_dtype(self, dtype) -> str:
        """Map pandas dtype to SQLite type.

        Args:
            dtype: Pandas dtype

        Returns:
            SQLite type string
        """
        dtype_str = str(dtype)
        if "int" in dtype_str:
            return "INTEGER"
        if "float" in dtype_str:
            return "REAL"
        if "object" in dtype_str or "str" in dtype_str:
            return "TEXT"
        if "datetime" in dtype_str:
            return "TEXT"  # SQLite stores datetime as TEXT or INTEGER
        if "bool" in dtype_str:
            return "INTEGER"
        return "TEXT"  # Default to TEXT for unknown types
