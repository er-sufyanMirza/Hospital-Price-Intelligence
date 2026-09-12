create OR REPLACE table count_records as
SELECT count(benchmark_category) from mart_medicare_comparison