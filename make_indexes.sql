create index if not exists idx_detail1 on details (scrape_time, game_number);

create index if not exists idx_summary1 on summary (scrape_time);