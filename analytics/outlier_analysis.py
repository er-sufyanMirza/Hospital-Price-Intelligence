import duckdb

DATABASE_PATH = 'data/processed/hospital_prices.duckdb'

def main():
    con = duckdb.connect(DATABASE_PATH)
    
    query = (
        """SELECT
                service_id,
                payer_count,
                min_negotiated_price,
                max_negotiated_price
                absolute_price_spread,
                relative_price_spread_pct,
                price_ratio,
                variation_category
                
            FROM mart_price_outliers
            
            ORDER BY price_ratio DESC;"""
    )
    
    result = con.execute(query).df()
    
    print("\nHOSPITAL PRICE OUTLIER ANALYSIS")
    print("="*110)
    
    print(result.to_string(index=False))
    
    con.close()
    
if __name__ == '__main__':
    main()
    
    