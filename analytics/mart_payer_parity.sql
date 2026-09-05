CREATE OR REPLACE TABLE mart_payer_parity AS

WITH dollar_prices AS (

    SELECT
        service_id,
        description,
        setting,
        payer_name,
        plan_name,
        negotiated_dollar

    FROM mart_price_variation

    WHERE charge_type = 'DOLLAR'
      AND negotiated_dollar IS NOT NULL
      AND negotiated_dollar > 0
),

service_summary AS (

    SELECT
        service_id,
        description,
        setting,

        COUNT(*) AS payer_count,

        MIN(negotiated_dollar)
            AS min_negotiated_price,

        MAX(negotiated_dollar)
            AS max_negotiated_price,

        AVG(negotiated_dollar)
            AS avg_negotiated_price,

        MEDIAN(negotiated_dollar)
            AS median_negotiated_price

    FROM dollar_prices

    GROUP BY
        service_id,
        description,
        setting
)

SELECT

    service_id,
    description,
    setting,

    payer_count,

    min_negotiated_price,
    max_negotiated_price,

    ROUND(
        avg_negotiated_price,
        2
    ) AS avg_negotiated_price,

    ROUND(
        median_negotiated_price,
        2
    ) AS median_negotiated_price,

    ROUND(
        max_negotiated_price
        - min_negotiated_price,
        2
    ) AS absolute_price_spread,

    ROUND(
        (
            max_negotiated_price
            - min_negotiated_price
        )
        / NULLIF(
            min_negotiated_price,
            0
        ) * 100,
        2
    ) AS relative_price_spread_pct,

    ROUND(
        max_negotiated_price
        / NULLIF(
            min_negotiated_price,
            0
        ),
        2
    ) AS price_ratio

FROM service_summary

WHERE payer_count >= 2;