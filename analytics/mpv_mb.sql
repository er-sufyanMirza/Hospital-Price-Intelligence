SELECT description, count(*) as null_count 
from mart_price_variation as p
from medicare_benchmark as b
INNER JOIN on p.description = b.description
group by description