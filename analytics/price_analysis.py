import duckdb

DATABASE_PATH = 'data/processed/hospital_prices.duckdb'

def payer_price_comparison():
    con = duckdb.connect(DATABASE_PATH)
    
    query = """
    SELECT
        s.description,
        p.payer_name,
        p.plan_name,
        p.charge_type,
        p.negotiated_dollar,
        p.negotiated_percentage,
        p.median_allowed_amount
    FROM payer_charge p
    
    INNER JOIN standard_charge c
        on p.charge_id = c.charge_id
    
    INNER JOIN service s
        on c.service_id = s.service_id
        
    ORDER BY
        s.description,
        p.payer_name;
        """
    return con.execute(query).df()

if __name__ == '__main__':
    result = payer_price_comparison()
    
    print(result.to_string(index=False))