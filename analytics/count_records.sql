create OR REPLACE table count_records as
SELECT benchmark_category count(*) 
from mart_medicare_comparison
group by benchmark_category;