CREATE OR REPLACE TABLE mart_methodology_summary AS

SELECT
    methodology,

    COUNT(*) AS negotiated_rate_count,
    COUNT(DISTINCT payer_name) AS payer_count,
    COUNT(DISTINCT plan_name) AS plan_count,

    ROUND(
        MIN(negotiated_dollar),2
    ) AS min_negotiated_dollar,

    ROUND(
        MAX(negotiated_dollar), 2
    ) AS max_negotiated_dollar,

    ROUND(
        AVG(negotiated_dollar), 2
    ) AS avg_negotiated_dollar,

    ROUND(
        MEDIAN(negotiated_dollar), 2
    ) AS median_negotiated_dollar,

FROM mart_price_variation

WHERE negotiated_dollar IS NOT NULL
    AND negotiated_dollar > 0

GROUP BY methodology

ORDER BY avg_negotiated_dollar DESC;