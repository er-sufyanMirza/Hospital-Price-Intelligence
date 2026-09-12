import duckdb

DATABASE_PATH = 'data/processed/hospital_prices.duckdb'
SQL_PATH = 'data/raw/medicare_benchmark_sample.csv'

def main():
    con = duckdb.connect(DATABASE_PATH)
    result = con.execute(
        """select count(*)
            from count_records
        """
    ).df()
    
    print(result.to_string(index=False))
    con.close()
    
if __name__ == '__main__':
    main()