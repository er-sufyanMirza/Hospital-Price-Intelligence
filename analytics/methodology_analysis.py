import duckdb

DATABASE_PATH = 'data/processed/hospital_prices.duckdb'

def main():
    con = duckdb.connect(DATABASE_PATH)
    
    query = """ 
    SELECT
        methodology,
        negotiated_rate_count,
        payer_count,
        plan_count,
        min_negotiated_dollar,
        max_negotiated_dollar,
        avg_negotiated_dollar,
        median_negotiated_dollar
    FROM mart_methodology_summary
    ORDER BY avg_negotiated_dollar DESC;"""
    
    result = con.execute(query).df()
    
    print("\nCONTRACT METHODOLOGY SUMMARY")
    print("="*100)
    
    print(result.to_string(index=False))
    
    con.close()
    
if __name__ == '__main__':
    main()