import duckdb


DATABASE_PATH = "data/processed/hospital_prices.duckdb"
SQL_PATH = "analytics/mart_medicare_comparison.sql"


def main():
    con = duckdb.connect(DATABASE_PATH)

    try:
        with open(SQL_PATH, "r", encoding="utf-8") as file:
            sql = file.read()

        con.execute(sql)

        count = con.execute(
            "SELECT COUNT(*) FROM mart_medicare_comparison"
        ).fetchone()[0]

        print(f"Created mart_medicare_comparison with {count} records.")

        print("\nMedicare comparison preview:")

        result = con.execute(
            """
            SELECT
                description,
                payer_name,
                plan_name,
                negotiated_dollar,
                medicare_benchmark_amount,
                difference_from_medicare,
                medicare_price_ratio,
                variance_from_medicare_pct,
                benchmark_category
            FROM mart_medicare_comparison
            ORDER BY medicare_price_ratio DESC
            """
        ).df()

        print(result.to_string(index=False))

    finally:
        con.close()


if __name__ == "__main__":
    main()