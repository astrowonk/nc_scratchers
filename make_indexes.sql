create index if not exists idx_detail1 on details (scrape_time, game_number);

create index if not exists idx_summary1 on summary (scrape_time);

drop view if exists fraction_remaining;

create view fraction_remaining as 
SELECT game_number, fraction_unclaimed,scrape_time
FROM (
    SELECT
        game_number,
        fraction_unclaimed,
        expectation_score,
        scrape_time,
        value,
        MIN(value) OVER (PARTITION BY game_number,scrape_time) AS min_value
    FROM details
)
WHERE expectation_score = 1
  AND value = min_value
ORDER BY fraction_unclaimed DESC;