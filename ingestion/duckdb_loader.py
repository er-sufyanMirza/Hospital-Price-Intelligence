from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


class DuckDBLoader:
    """Load normalized MRF DataFrames into DuckDB."""

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def load_tables(
        self,
        tables: dict[str, pd.DataFrame],
    ) -> None:
        """Create or replace DuckDB tables."""

        connection = duckdb.connect(
            str(self.database_path)
        )

        try:
            for table_name, dataframe in tables.items():

                connection.register(
                    f"{table_name}_df",
                    dataframe,
                )

                connection.execute(
                    f"""
                    CREATE OR REPLACE TABLE
                    {table_name}
                    AS
                    SELECT *
                    FROM {table_name}_df
                    """
                )

                connection.unregister(
                    f"{table_name}_df"
                )

        finally:
            connection.close()