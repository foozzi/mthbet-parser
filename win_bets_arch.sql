BEGIN TRANSACTION;
CREATE TABLE win_bets (id INTEGER PRIMARY KEY, season INTEGER, tour INTEGER, kof INTEGER, date_parse DATE);
CREATE INDEX tour_
ON win_bets (tour);
CREATE INDEX season_
ON win_bets (season);
CREATE INDEX kof_
ON win_bets (kof);
COMMIT;
