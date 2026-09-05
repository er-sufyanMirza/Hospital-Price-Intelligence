import duckdb
import pandas as pd


DATABASE_PATH = "data/processed/hospital_prices.duckdb"
BENCHMARK_PATH = "data/raw/medicare_benchmark_sample.csv"


def main():
    # Read benchmark CSV with pandas
    benchmark_df = pd.read_csv(BENCHMARK_PATH)

    # Basic validation
    required_columns = {
        "description",
        "benchmark_type",
        "medicare_benchmark_amount",
        "source_status",
    }

    missing_columns = required_columns - set(benchmark_df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required benchmark columns: {sorted(missing_columns)}"
        )

    # Ensure numeric benchmark values
    benchmark_df["medicare_benchmark_amount"] = pd.to_numeric(
        benchmark_df["medicare_benchmark_amount"],
        errors="coerce",
    )

    if benchmark_df["medicare_benchmark_amount"].isna().any():
        raise ValueError(
            "One or more Medicare benchmark amounts are not numeric."
        )

    # Connect to DuckDB
    con = duckdb.connect(DATABASE_PATH)

    try:
        # Remove previous version
        con.execute("DROP TABLE IF EXISTS medicare_benchmark")

        # Register pandas DataFrame
        con.register("benchmark_df", benchmark_df)

        # Create DuckDB table
        con.execute(
            """
            CREATE TABLE medicare_benchmark AS
            SELECT
                description,
                benchmark_type,
                medicare_benchmark_amount,
                source_status
            FROM benchmark_df
            """
        )

        # Confirm record count
        count = con.execute(
            "SELECT COUNT(*) FROM medicare_benchmark"
        ).fetchone()[0]

        print(f"Loaded {count} Medicare benchmark records.")

        # Preview
        print("\nBenchmark preview:")

        preview = con.execute(
            """
            SELECT *
            FROM medicare_benchmark
            LIMIT 5
            """
        ).df()

        print(preview.to_string(index=False))

    finally:
        con.close()


if __name__ == "__main__":
    main()