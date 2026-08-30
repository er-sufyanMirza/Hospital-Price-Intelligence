from __future__ import annotations

import duckdb
import pandas as pd


DATABASE_PATH = "data/processed/hospital_prices.duckdb"


def profile_tables() -> pd.DataFrame:
    con = duckdb.connect(DATABASE_PATH)

    tables = con.execute(
        "SHOW TABLES"
    ).fetchdf()

    rows = []

    for table_name in tables["name"]:

        count = con.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        columns = con.execute(
            f"DESCRIBE {table_name}"
        ).fetchdf()

        rows.append(
            {
                "table_name": table_name,
                "row_count": count,
                "column_count": len(columns),
            }
        )

    con.close()

    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(
        profile_tables().to_string(
            index=False
        )
    )