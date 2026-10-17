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

drop view if exists latest_top_prizes;

create view latest_top_prizes as
WITH latest AS (
    SELECT *
    FROM details
    WHERE scrape_time = (
        SELECT MAX(scrape_time)
        FROM details
    )
),
ranked AS (
    SELECT *,
           RANK() OVER (
               PARTITION BY game_number
               ORDER BY value DESC
           ) AS rnk
    FROM latest
)
SELECT
    game_number,
    SUM(winners_remaining) AS top_prizes_left
FROM ranked
WHERE rnk = 1
GROUP BY game_number;

drop view if exists summary_view;
create view summary_view as 

select
	s.*,
	fraction_unclaimed,
	tp.top_prizes_left as top_prizes_remaining
from
	summary s
left join fraction_remaining fr on
	fr.scrape_time = s.scrape_time
	and fr.game_number = s.game_number
left join latest_top_prizes tp on 
	tp.game_number = s.game_number
where
	s.scrape_time = (
	SELECT
		MAX(scrape_time)
	FROM
		summary)
order by
	current_expectation_value desc;