
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

"""
Todo:
1. Basic data: Champions that are good at 
(1). killing tower
(2). first blood
(3). monster KILLER(baron or dragon) [大龙杀手，小龙杀手，蓝爸爸红爸爸杀手], or 杀敌方野怪[最擅长入侵]最多
(4). panta kill／。。。
(5). 最肉tank [take most physical/magic//true demage ]
(6). 最高输出 (physical/magic/true)
(7). 补兵最多
(8). 死的最多／存活率[时间]最高
(9). 助攻王/击杀王
(10). 控场王[timeCC]
(11). 最容易连杀
(12). 死亡频率较高[hidden senior case: 分析死亡数与消极游戏的联系]
(13). most wards brought/killed (sight/vision) [插言／排眼，是一个好辅助的重要因素之一]
(14). 最能奶的英雄(heal)
(15). 红蓝方谁更容易赢
(16). 推塔数／大龙数[baron]／小龙数[dragon]/峡谷先锋 与比赛输赢的关系
(17). 暴击王
2. 进阶data:
(1). Big mistake, miss Skin!! Forgot to make it! [most popular skin, every hero's most popular skin, relationship between skin and win rate]
(2). 英雄常用装备分析，推荐[游戏内已提供]
(3). 英雄相克[交手战绩，杀／被杀次数，对线情况] ***
(4). 最适合搭配队友[其实游戏中已被提供](可以个性化)  ****
(5). 英雄走哪条路线胜率高 ***
(6). 哪些是大后期，哪些后期废物(经济／输出比)
(7). 利用kda，双方经济比，人头比预测比赛输赢  ****
(8). 分析哪一路在游戏中最重要 (哪一路的双方经济／人头比对比赛结果影响最大)
(9). 哪些英雄逆风局最容易翻盘(对敌方英雄输出最高，己方具有主要经济输出击杀等，己方总体经济／击杀落后于对方但最终取得胜利)
(10). 英雄分类（战士，坦克，法师，射手，辅助，刺客。。。） *****

3. 高级分析
(1). 英雄个性化推荐
(2). 召唤师技能[summoner spell]智能推荐,综合考虑每个英雄，走不同路线，对战不同英雄
(3). 预测比赛输赢(同2.7)

"""

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
print(champion)

all_data = []
for c in champion:
    all_data.append(champion_data(c[0], participants))
    print(c[1],champion_data(c[0], participants))
print(all_data)


