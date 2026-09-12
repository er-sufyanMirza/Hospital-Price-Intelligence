import duckdb

DATABASE_PATH = 'data/processed/hospital_prices.duckdb'

def main():
    con = duckdb.connect(DATABASE_PATH)
    
    query = con.sql("""
                    select count(*) as null_count 
                    from mart_price_variation as p 
                    left join medicare_benchmark as b on 
                    p.description = b.description
                    where b.description is null 
                    and p.charge_type = 'DOLAAR'
                    and p.negotiated_dollar is not null
                    and p.negotiated_dollar > 0
                    """).df()
    print(query.to_string(index=False))
    con.close()

if __name__ == '__main__':
    main()
    