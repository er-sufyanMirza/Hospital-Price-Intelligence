import duckdb

DATABASE_PATH = 'data/processed/hospital_prices.duckdb'

MARTS = ['analytics/mart_price_variation.sql',
         'analytics/mart_payer_parity.sql',
         'analytics/mart_price_outliers.sql',
         'analytics/mart_methodology_summary.sql',
         'analytics/mart_medicare_comparison.sql']

def build_marts():
    con = duckdb.connect(DATABASE_PATH)
    
    try:
        for sql_path in MARTS:
            print(f"Building {sql_path}...")
            
            with open(sql_path, 'r', encoding='utf-8')as file:
                sql = file.read()
                
            con.execute(sql)
            
            print('complete')
            
    finally:
        print("\nAll analytical marts built.")
        
if __name__ == '__main__':
    build_marts()
            
            