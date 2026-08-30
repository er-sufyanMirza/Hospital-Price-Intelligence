from ingestion.duckdb_loader import DuckDBLoader
from ingestion.json_parser import MRFParser


MRF_PATH = "data/raw/west_mercy_v3.json"
DATABASE_PATH = "data/processed/hospital_prices.duckdb"


def main():
    print("Loading MRF...\n")

    parser = MRFParser(MRF_PATH)
    tables = parser.parse()

    print("Parsed tables:")

    for name, dataframe in tables.items():
        print(
            f" {name:<20}"
            f"{len(dataframe):>6} rows"
        )

    print("\nLoading DuckDB...")

    loader = DuckDBLoader(DATABASE_PATH)
    loader.load_tables(tables)

    print(f"\nLoaded {len(tables)} tables.")

    print(
        "\nDatabase created:"
        f"\n{DATABASE_PATH}"
    )


if __name__ == "__main__":
    main()