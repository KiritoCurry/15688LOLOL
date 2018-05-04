import sqlite3
import pandas as pd
import math
import time
import random

import cassiopeia as cass
from cassiopeia import Summoner, Match, Champions
from cassiopeia.data import Season, Queue, Tier

conn = sqlite3.connect('lol.db')
s=pd.read_sql('SELECT * FROM CHAMPION WHERE id={}'.format(123),conn).empty
c=conn.cursor()
c.execute("select * from item ")
conn.commit()
conn.commit()
a=pd.read_sql("select name from item ",conn)
print(len(list(a['name'])))
print(s)