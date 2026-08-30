CREATE OR REPLACE TABLE mart_price_variation AS

SELECT
    s.service_id,
    s.description,

    c.charge_id,
    c.setting,

    c.minimum,
    c.maximum,
    c.gross_charge,
    c.discounted_cash,

    p.payer_charge_id,
    p.payer_name,
    p.plan_name,
    p.methodology,
    p.charge_type,

    p.negotiated_dollar,
    p.negotiated_percentage,
    p.negotiated_algorithm,

    p.median_allowed_amount,
    p.p10_allowed_amount,
    p.p90_allowed_amount,
    p.allowed_amount_count,

    CASE
        WHEN p.charge_type = 'DOLLAR'
            AND c.gross_charge > 0
        THEN
            1- (negotiated_dollar/gross_charge)
        ELSE NULL

    END AS negotiated_discount_pct,

    CASE
        WHEN c.gross_charge > 0
        THEN
            1-(c.discounted_cash/c.gross_charge)
        ELSE NULL
        END AS cash_discount_pct

    FROM payer_charge p

INNER JOIN standard_charge c
    on p.charge_id = c.charge_id

INNER JOIN service s
    on c.service_id = s.service_id