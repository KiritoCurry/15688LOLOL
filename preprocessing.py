
# coding: utf-8

# import cassiopeia as cass

# from cassiopeia.data import Queue, GameMode, Season
# from cassiopeia import SummonerSpell, SummonerSpells
# import arrow
# from cassiopeia.core import Summoner, MatchHistory, Match
import sqlite3
import pandas as pd
import numpy as np
from collections import Counter

conn = sqlite3.connect('lol.db')
def get_data(conn, table_name):
    res = []
    query = 'SELECT * FROM ' + table_name
    c = conn.cursor()
    data = c.execute(query)
    for d in data:
        res.append(d)
    return res

def get_position(p):
    if p[7] == 'BOT_LANE' or None:
        if p[6] == 'DUO':
            return None
        else:
            return p[6]
    else:
        return p[7]


def ban_rate(champion_id, team_ban):
    champions = []
    for ban in team_ban:
        champions.append(ban[-1])
    rate = champions.count(champion_id)/len(team_ban)
    return rate

def champion_data(champion_id, participants):
    chosen_rate = {}
    win_rate = {}
    kill = {}
    death = {}
    assist = {}
    damage_to = {}
    damage_taken = {}
    gold = {}
    res = {}
    for p in participants:
        if p[3] == champion_id:
            pos = get_position(p)
            if pos is None:
                continue
            else:
                if pos in chosen_rate:
                    chosen_rate[pos]+=1
                    win_rate[pos].append(p[5])
                    kill[pos].append(p[12])
                    death[pos].append(p[13])
                    assist[pos].append(p[14])
                    damage_to[pos].append(p[-6])
                    damage_taken[pos].append(p[-5])
                    gold[pos].append(p[26])
                    
                else:
                    chosen_rate[pos] = 1
                    win_rate[pos] = []
                    kill[pos] = []
                    death[pos] = []
                    assist[pos] = []
                    damage_to[pos] = []
                    damage_taken[pos] = []
                    gold[pos] = []
                    chosen_rate[pos]+=1
                    win_rate[pos].append(p[5])
                    kill[pos].append(p[12])
                    death[pos].append(p[13])
                    assist[pos].append(p[14])
                    damage_to[pos].append(p[-6])
                    damage_taken[pos].append(p[-5])
                    gold[pos].append(p[26])
                    
    for r in chosen_rate:
        rate = chosen_rate[r]/len(participants)
        res[r] = []
        res[r].append({'chosen_rate': rate})
    for r in win_rate:
        rate = sum(win_rate[r])/len(win_rate[r])
        res[r].append({'win_rate': rate})
    for k in kill:
        res[k].append({'kills': sum(kill[k])/len(kill[k])})
    for d in death:
        res[d].append({'deaths': sum(death[d])/len(death[d])})
    for a in assist:
        res[a].append({'assists': sum(assist[a])/len(assist[a])})
    for d in damage_to:
        res[d].append({'total_damage_to': sum(damage_to[d])/len(damage_to[d])})
    for d in damage_taken:
        res[d].append({'total_damage_taken': sum(damage_taken[d])/len(damage_taken[d])})
    for g in gold:
        res[g].append({'gold_earned': sum(gold[g])/len(gold[g])})
    
    return res



participants = get_data(conn, 'Participants')
champion = get_data(conn, 'Champion')
ban = get_data(conn, 'team_ban')

all_data = []
for c in champion:
    all_data.append(champion_data(c[0], participants))
print(all_data)


