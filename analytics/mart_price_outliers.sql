CREATE OR REPLACE TABLE mart_price_outliers AS

SELECT
    service_id,
    description,
    setting,

    payer_count,

    min_negotiated_price,
    max_negotiated_price,
    avg_negotiated_price,
    median_negotiated_price,

    absolute_price_spread,
    relative_price_spread_pct,
    price_ratio,

    CASE
        WHEN price_ratio >=5
        THEN 'EXTREME'

        WHEN price_ratio >=2
        THEN 'HIGH'

        WHEN price_ratio >=1.5
        THEN 'MODERATE'

        ELSE 'LOW'

    END AS variation_category

FROM mart_payer_parity;
