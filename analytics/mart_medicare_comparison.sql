CREATE OR REPLACE TABLE mart_medicare_comparison AS

SELECT
    p.description,
    p.payer_name,
    p.plan_name,
    p.negotiated_dollar,

    b.medicare_benchmark_amount,

    ROUND(
        p.negotiated_dollar - b.medicare_benchmark_amount,
        2
    ) AS difference_from_medicare,

    ROUND(
        p.negotiated_dollar /
        NULLIF(b.medicare_benchmark_amount, 0),
        2
    ) AS medicare_price_ratio,

    ROUND(
        (
            (
                p.negotiated_dollar -
                b.medicare_benchmark_amount
            )
            / NULLIF(b.medicare_benchmark_amount, 0)
        ) * 100,
        2
    ) AS variance_from_medicare_pct,

    CASE
        WHEN p.negotiated_dollar < b.medicare_benchmark_amount
            THEN 'BELOW_BENCHMARK'

        WHEN p.negotiated_dollar <= b.medicare_benchmark_amount * 1.25
            THEN 'NEAR_BENCHMARK'

        WHEN p.negotiated_dollar <= b.medicare_benchmark_amount * 1.50
            THEN 'ELEVATED'

        ELSE 'HIGH'
    END AS benchmark_category,

    b.benchmark_type,
    b.source_status

FROM mart_price_variation AS p

INNER JOIN medicare_benchmark AS b
    ON LOWER(TRIM(p.description))
       = LOWER(TRIM(b.description))

WHERE p.charge_type = 'DOLLAR'
  AND p.negotiated_dollar IS NOT NULL
  AND p.negotiated_dollar > 0;