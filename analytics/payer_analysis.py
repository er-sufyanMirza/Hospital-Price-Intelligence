import duckdb


DATABASE_PATH = (
    "data/processed/hospital_prices.duckdb"
)


def main():

    con = duckdb.connect(
        DATABASE_PATH
    )

    query = """
        SELECT
            description,
            payer_count,
            min_negotiated_price,
            max_negotiated_price,
            avg_negotiated_price,
            absolute_price_spread,
            relative_price_spread_pct,
            price_ratio
        FROM mart_payer_parity
        ORDER BY relative_price_spread_pct DESC;
    """

    result = con.execute(query).df()

    print("\nPAYER PRICE PARITY ANALYSIS")
    print("=" * 100)

    print(
        result.to_string(
            index=False
        )
    )

    con.close()


if __name__ == "__main__":
    main()