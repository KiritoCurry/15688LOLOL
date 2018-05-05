import sqlite3
import pandas as pd
import math
import time
import random
from collections import Counter

import cassiopeia as cass
from cassiopeia import Summoner, Match, Champions
from cassiopeia.data import Season, Queue, Tier

conn = sqlite3.connect('lol.db')
# s = pd.read_sql('SELECT * FROM CHAMPION WHERE id={}'.format(123), conn).empty
c = conn.cursor()
# c.execute("SELECT * FROM item ")
c.execute("SELECT * FROM MATCH WHERE id={}".format(2699934038))
conn.commit()
# conn.commit()
# conn.commit()
# a = pd.read_sql("select name from item ", conn)
# print(len(list(a['name'])))
# print(s)
# s1 = "pid, summoner_id, match_id, champion_id, side, win, role, lane, sspell1, sspell2, level, items, kills,deaths,assist,kda, turret_kills, first_tower_kill, damage_dealt_to_turrets, first_blood_kill, double_kills,triple_kills,quadra_kills, penta_kills, killing_sprees, inhibitor_kills, gold_earned, gold_spent,largest_killing_spree, largest_critical_strike, largest_multi_kill, longest_time_spent_living,magic_damage_dealt_to_champions, magical_damage_taken, neutral_minions_killed,neutral_minions_killed_enemy_jungle, physical_damage_dealt_to_champions, physical_damage_taken,sight_wards_bought_in_game, total_damage_dealt_to_champions, total_damage_taken, total_heal,total_minions_killed, true_damage_dealt_to_champions, true_damage_taken, vision_wards_bought_in_game,wards_killed, wards_placed, time_CCing_others"
# print(len(s1.split(',')))
# a=['123','123','asd','qwe']
# b=Counter(a)
# c=b.most_common(1)
# print(c[0][0])