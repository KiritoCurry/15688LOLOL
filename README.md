# 15688LOLOL
15688 final project.

To run this the crawler successfully, you need to pay attention to:
1. Support sqlite. Extremely recommend you to install SQLPro for SQLite so that you will have a clear understanding of what the data is like.
2. Before run the crawler, create a db file called lol.db first, then run the lol.sql script either in sqlpro for sqlite(recommended!) or by sqlite3.executescript method.
all the two files should be put in the same directory as the crawler.
3. After you install cassiopeia, you need to modify two place in the source code to correctly fetch the data.
Find where you install it(mine is in ~/anaconda3/lib/python3.6/site-packages/cassiopeia/core),then
(1). match.py, line 1053, find function def time_CCing_others(self) -> int:, change return to "return self._data[ParticipantStatsData].timeCCingOthers"
(2). summoner.py, line 222, find function def rank_last_season(self):, change return to "return most_recent_match.participants[self.name].rank_last_season".
