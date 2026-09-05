import duckdb


DATABASE_PATH = "data/processed/hospital_prices.duckdb"


def main():
    con = duckdb.connect(DATABASE_PATH)

    query = """
        SELECT
            s.description,
            pc.payer_name,
            pc.plan_name,
            pc.methodology,
            pc.negotiated_dollar,
            pc.negotiated_percentage,
            pc.additional_payer_notes

        FROM payer_charge AS pc

        JOIN standard_charge AS sc
            ON pc.charge_id = sc.charge_id

        JOIN service AS s
            ON sc.service_id = s.service_id

        WHERE LOWER(s.description) LIKE '%inguinal hernia%'

        ORDER BY
            pc.negotiated_dollar DESC;
    """

    result = con.execute(query).df()

    print("\nINGUINAL HERNIA PRICE INVESTIGATION")
    print("=" * 110)

    print(result.to_string(index=False))

    con.close()


if __name__ == "__main__":
    main()