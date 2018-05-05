
# coding: utf-8

import sqlite3
import pandas as pd
import numpy as np
# import cassiopeia as cass
# from cassiopeia.data import Queue, GameMode, Season
# from cassiopeia import SummonerSpell, SummonerSpells
# import arrow
# from cassiopeia.core import Summoner, MatchHistory, Match
# from collections import Counter
# import json
# import time
# import csv

conn = sqlite3.connect('lol.db')

def get_data(conn, table_name):
    res = []
    query = 'SELECT * FROM ' + table_name
    c = conn.cursor()
    data = c.execute(query)
    for d in data:
        res.append(d)
    return res

def chosen_rate(champion_id, participants):
    data = {}
    res = {}
    for p in participants:
        if p[3] == champion_id:
            pos = get_position(p)
            if pos is None:
                continue
            else:
                if pos in data:
                    data[pos]+=1
                else:
                    data[pos]=1
    for each in data:
        rate = data[each]/len(participants)
        res[each] = rate
    return res

def get_position(p):
    if p[7] == 'BOT_LANE' or None:
        if p[6] == 'DUO':
            return None
        else:
            return p[6]
    else:
        return p[7]


def win_rate(champion_id, participants):
    data = {}
    res = {}
    for p in participants:
        if p[3] == champion_id:
            pos = get_position(p)
            if pos is None:
                continue
            else:
                if pos in data:
                    data[pos].append(p[5])
                else:
                    data[pos] = []
                    data[pos].append(p[5])
    for each in data:
        rate = sum(data[each])/len(data[each])
        res[each] = rate
    return res

def ban_rate(champion_id, team_ban):
    champions = []
    for ban in team_ban:
        champions.append(ban[-1])
    rate = champions.count(champion_id)/len(team_ban)
    return rate

def average_kda(champion_id, participants):
    kill = {}
    death = {}
    assist = {}
    res = {}
    for p in participants:
        if p[3] == champion_id:
            pos = get_position(p)
            if pos is None:
                continue
            else:
                if pos in kill:
                    kill[pos].append(p[12])
                    death[pos].append(p[13])
                    assist[pos].append(p[14])
                else:
                    kill[pos] = []
                    death[pos] = []
                    assist[pos] = []
                    kill[pos].append(p[12])
                    death[pos].append(p[13])
                    assist[pos].append(p[14])
    for k in kill:
        res[k] = sum(kill[k])/len(kill[k])
    for d in death:
        res[d] = sum(death[d])/len(death[d])
    for a in assist:
        res[a] = sum(assist[a])/len(assist[a])
    
    return res

def damage(champion_id, participants):
    damage_to = {}
    damage_taken = {}
    res1 = {}
    res2 = {}
    for p in participants:
        if p[3] == champion_id:
            pos = get_position(p)
            if pos is None:
                continue
            else:
                if pos in damage_to:
                    damage_to[pos].append(p[-6])
                    damage_taken[pos].append(p[-5])
                else:
                    damage_to[pos] = []
                    damage_taken[pos] = []
                    damage_to[pos].append(p[-6])
                    damage_taken[pos].append(p[-5])
    for d in damage_to:
        res1[d] = sum(damage_to[d])/len(damage_to[d])
    for d in damage_taken:
        res2[d] = sum(damage_taken[d])/len(damage_taken[d])
    return res1, res2
    
def money(champion_id, participants):
    gold = {}
    res = {}
    for p in participants:
        if p[3] == champion_id:
            pos = get_position(p)
            if pos is None:
                continue
            else:
                if pos in gold:
                    gold[pos].append(p[26])
                else:
                    gold[pos] = []
                    gold[pos].append(p[26])
    for g in gold:
        res[g] = sum(gold[g])/len(gold[g])
    return res


participants = get_data(conn, 'Participants')
champion = get_data(conn, 'Champion')
ban = get_data(conn, 'team_ban')

chosen_rates = []
ban_rates = []
win_rates = []
average_kdas = []
average_damage_to = []
average_damage_taken = []
moneys = []

for c in champion:
    chosen_rates.append(chosen_rate(c[0], participants))
    ban_rates.append(ban_rate(c[0], ban))
    win_rates.append(win_rate(c[0], participants))
    average_kdas.append(average_kda(c[0], participants))
    average_damage_to.append(damage(c[0], participants)[0])
    average_damage_taken.append(damage(c[0], participants)[1])
    moneys.append(money(c[0], participants))

# print(chosen_rates)
# print(win_rates)
# print(max(ban_rates))
# print(average_kdas)
# print(moneys)

