import duckdb

DATABASE_PATH = 'data/processed/hospital_prices.duckdb'

SQL_PATH = 'analytics/mart_price_variation.sql'

def build_price_variation_mart():
    con = duckdb.connect(DATABASE_PATH)
    
    with open(SQL_PATH, 'r', encoding='utf-8') as file:
        sql = file.read()
        
        con.execute(sql)
        
        count = con.execute(
    """
    SELECT COUNT(*)
    FROM mart_price_variation
    """
        ).fetchone()[0]
        
        con.close()
        
        print("mart price variation created")
        
        print(f"Rows:{count}")
        
if __name__ == '__main__':
    build_price_variation_mart()