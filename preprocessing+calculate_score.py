import sqlite3
import pandas as pd
import numpy as np
from collections import Counter
# import cassiopeia as cass
# from cassiopeia.data import Queue, GameMode, Season
# from cassiopeia import SummonerSpell, SummonerSpells
# import arrow
# from cassiopeia.core import Summoner, MatchHistory, Match
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
    physical_damage_to = {}
    physical_damage_taken = {}
    magic_damage_to = {}
    magic_damage_taken = {}
    true_damage_to = {}
    true_damage_taken = {}
    gold_earned = {}
    gold_spent = {}
    tower_kill = {}
    minions_kill = {}
    minions_kill_enemy = {}
    first_blood = {}
    total_heal = {}
    time_CCing = {}
    sight_ward = {}
    vision_ward = {}
    wards_killed = {}
    wards_placed = {}
    largest_killing_spree = {}
    largest_critical_strike = {}
    largest_multi_kill = {}
    longest_living_time = {}
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
                    physical_damage_to[pos].append(p[36])
                    physical_damage_taken[pos].append(p[37])
                    magic_damage_to[pos].append(p[32])
                    magic_damage_taken[pos].append(p[33])
                    true_damage_to[pos].append(p[-6])
                    true_damage_taken[pos].append(p[-5])
                    gold_earned[pos].append(p[26])
                    gold_spent[pos].append(p[27])
                    tower_kill[pos].append(p[16])
                    minions_kill[pos].append(p[34])
                    minions_kill_enemy[pos].append(p[35])
                    first_blood[pos].append(p[19])
                    total_heal[pos].append(p[-8])
                    time_CCing[pos].append(p[-1])
                    sight_ward[pos].append(p[-11])
                    vision_ward[pos].append(p[-4])
                    wards_killed[pos].append(p[-3])
                    wards_placed[pos].append(p[-2])
                    largest_killing_spree[pos].append(p[28])
                    largest_critical_strike[pos].append(p[29])
                    largest_multi_kill[pos].append(p[30])
                    longest_living_time[pos].append(p[31])
                    
                    
                else:
                    chosen_rate[pos] = 1
                    win_rate[pos] = []
                    kill[pos] = []
                    death[pos] = []
                    assist[pos] = []
                    physical_damage_to[pos] = []
                    physical_damage_taken[pos] =[]
                    magic_damage_to[pos] = []
                    magic_damage_taken[pos] = []
                    true_damage_to[pos] = []
                    true_damage_taken[pos] = []
                    gold_earned[pos] = []
                    gold_spent[pos] = []
                    tower_kill[pos] = []
                    minions_kill[pos] = []
                    minions_kill_enemy[pos] = []
                    first_blood[pos] = []
                    total_heal[pos] = []
                    time_CCing[pos] = []
                    sight_ward[pos] = []
                    vision_ward[pos] = []
                    wards_killed[pos] = []
                    wards_placed[pos] = []
                    largest_killing_spree[pos] = []
                    largest_critical_strike[pos] = []
                    largest_multi_kill[pos] = []
                    longest_living_time[pos] = []

                    chosen_rate[pos]+=1
                    win_rate[pos].append(p[5])
                    kill[pos].append(p[12])
                    death[pos].append(p[13])
                    assist[pos].append(p[14])
                    physical_damage_to[pos].append(p[36])
                    physical_damage_taken[pos].append(p[37])
                    magic_damage_to[pos].append(p[32])
                    magic_damage_taken[pos].append(p[33])
                    true_damage_to[pos].append(p[-6])
                    true_damage_taken[pos].append(p[-5])
                    gold_earned[pos].append(p[26])
                    gold_spent[pos].append(p[27])
                    tower_kill[pos].append(p[16])
                    minions_kill[pos].append(p[34])
                    minions_kill_enemy[pos].append(p[35])
                    first_blood[pos].append(p[19])
                    total_heal[pos].append(p[-8])
                    time_CCing[pos].append(p[-1])
                    sight_ward[pos].append(p[-11])
                    vision_ward[pos].append(p[-4])
                    wards_killed[pos].append(p[-3])
                    wards_placed[pos].append(p[-2])
                    largest_killing_spree[pos].append(p[28])
                    largest_critical_strike[pos].append(p[29])
                    largest_multi_kill[pos].append(p[30])
                    longest_living_time[pos].append(p[31])
                    
                    
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
    for d in physical_damage_to:
        res[d].append({'physical_damage_to': sum(physical_damage_to[d])/len(physical_damage_to[d])})
    for d in physical_damage_taken:
        res[d].append({'physical_damage_taken': sum(physical_damage_taken[d])/len(physical_damage_taken[d])})
    
    for d in magic_damage_to:
        res[d].append({'magic_damage_to': sum(magic_damage_to[d])/len(magic_damage_to[d])})
    for d in magic_damage_taken:
        res[d].append({'magic_damage_taken': sum(magic_damage_taken[d])/len(magic_damage_taken[d])})
    for d in true_damage_to:
        res[d].append({'true_damage_to': sum(true_damage_to[d])/len(true_damage_to[d])})
    for d in true_damage_taken:
        res[d].append({'true_damage_taken': sum(true_damage_taken[d])/len(true_damage_taken[d])})
    for g in gold_earned:
        res[g].append({'gold_earned': sum(gold_earned[g])/len(gold_earned[g])})
    for g in gold_spent:
        res[g].append({'gold_spent': sum(gold_spent[g])/len(gold_spent[g])})
    for t in tower_kill:
        res[t].append({'tower_kill': sum(tower_kill[t])/len(tower_kill[t])})
    for t in minions_kill:
        res[t].append({'minions_kill': sum(minions_kill[t])/len(minions_kill[t])})
    for t in minions_kill_enemy:
        res[t].append({'minions_kill_enemy': sum(minions_kill_enemy[t])/len(minions_kill_enemy[t])})
    for t in first_blood:
        res[t].append({'first_blood': sum(first_blood[t])/len(first_blood[t])})
    
    for t in total_heal:
        res[t].append({'total_heal': sum(total_heal[t])/len(total_heal[t])})
    for t in time_CCing:
        res[t].append({'time_CCing': sum(time_CCing[t])/len(time_CCing[t])})
    for t in sight_ward:
        res[t].append({'sight_ward': sum(sight_ward[t])/len(sight_ward[t])})
    for t in vision_ward:
        res[t].append({'vision_ward': sum(vision_ward[t])/len(vision_ward[t])})
    for t in wards_killed:
        res[t].append({'wards_killed': sum(wards_killed[t])/len(wards_killed[t])})
    for t in wards_placed:
        res[t].append({'wards_placed': sum(wards_placed[t])/len(wards_placed[t])})
    for t in largest_killing_spree:
        res[t].append({'largest_killing_spree': sum(largest_killing_spree[t])/len(largest_killing_spree[t])})
    for t in largest_critical_strike:
        res[t].append({'largest_critical_strike': sum(largest_critical_strike[t])/len(largest_critical_strike[t])})
    for t in largest_multi_kill:
        res[t].append({'largest_multi_kill': sum(largest_multi_kill[t])/len(largest_multi_kill[t])})
    for t in longest_living_time:
        res[t].append({'longest_living_time': sum(longest_living_time[t])/len(longest_living_time[t])})
    
    return res


participants = get_data(conn, 'Participants')
champion = get_data(conn, 'Champion')
ban = get_data(conn, 'team_ban')
# kill_monster_event = get_data(conn, 'kill_monster_event')
train = participants[0:10400]
test = participants[10400:]
train_data = []
# test_data = {}
for c in champion:
    train_data.append(champion_data(c[0], train))
# print(train_data)

def calculate_rate(data, average):
    if data == 0:
        return 0
    return (data-average)/data

def calculate_score(data_set, position):
    train_scores = []
    sums = []
    for i in range(len(data_set)):
        d = data_set[i]
        try:
            if position[i] == 'JUNGLE':
                s = 10*d[0]+8*d[1]-8*d[2]+6*d[3] +8*d[4]+8*d[5]+6*d[6]+8*d[7]+10*d[8]+10*d[9] 
                +8*d[10]-6*d[11] +4*d[12]+10*d[13]+10*d[14] +4*d[15]+6*d[16]+6*d[17]
                +d[18]+d[19]+d[20]+d[21]+6*d[22]+6*d[23]+6*d[24]+6*d[25]
                sums.append(s)

            elif position[i] == 'TOP_LANE':
                s = 10*d[0]+8*d[1]-8*d[2]+6*d[3] +8*d[4]+8*d[5]+6*d[6]+8*d[7]+10*d[8]+10*d[9]
                +8*d[10]-6*d[11] +8*d[12]+8*d[13]+8*d[14] +6*d[15]+6*d[16]+6*d[17]
                +2*d[18]+2*d[19]+2*d[20]+2*d[21]+6*d[22]+6*d[23]+6*d[24]+6*d[25]
                sums.append(s)

            elif position[i] == 'MID_LANE':
                s = 10*d[0]+8*d[1]-8*d[2]+6*d[3]+6*d[4]+6*d[5]+12*d[6]+6*d[7]+10*d[8]+10*d[9]
                +8*d[10]-6*d[11] +8*d[12]+5*d[13]+5*d[14] +6*d[15]+6*d[16]+6*d[17]
                +2*d[18]+2*d[19]+2*d[20]+2*d[21]+6*d[22]+6*d[23]+6*d[24]+6*d[25]
                sums.append(s)

            elif position[i] == 'DUO_CARRY':
                s = 10*d[0]+8*d[1]-8*d[2]+6*d[3]+8*d[4]+8*d[5]+6*d[6]+8*d[7]+10*d[8]+10*d[9]
                +8*d[10]-6*d[11] +6*d[12]+6*d[13]+6*d[14] +6*d[15]+6*d[16]+6*d[17]
                +2*d[18]+2*d[19]+2*d[20]+2*d[21]+6*d[22]+6*d[23]+6*d[24]+6*d[25]
                sums.append(s)

            elif position[i] == 'DUO_SUPPORT':
                s = 2*d[0]+2*d[1]-2*d[2]+1.5*d[3]+8*d[4]+8*d[5]+6*d[6]+8*d[7]+10*d[8]+10*d[9]
                +8*d[10]-6*d[11] +6*d[12]+6*d[13]+6*d[14] +6*d[15]+6*d[16]+6*d[17]
                +6*d[18]+6*d[19]+6*d[20]+6*d[21]+4*d[22]+4*d[23]+4*d[24]+4*d[25]
                sums.append(s)
        except TypeError:
            sums.append('unknown')
            
#     print(sums)
    nums = []
    for i in sums:
        if i != 'unknown':
            nums.append(i)
    maxi = max(nums)
    mini = min(nums)
    for s in sums:
        if s != 'unknown':
            unit = 98/(maxi-mini)
            train_scores.append((s-mini)*unit + 1)
        else:
            train_scores.append(0)
    return train_scores    

train_rate = []
positions = []


for each in train[0:1000]:
    champion_datas = train_data[each[3]]
    if each[6] in champion_datas:
        champion_datas = champion_datas[each[6]]
        positions.append(each[6])
    elif each[7] in champion_datas:
        champion_datas = champion_datas[each[7]]
        positions.append(each[7])
    else:
        train_rate.append(0)
        positions.append(each[6])
        continue
    parti_data = [each[5], each[12], each[13], each[14], each[-9], each[-8], each[-13], each[-12], each[-6], each[-5],
                 each[26], each[27], each[16], each[-11], each[-10], each[19], each[-8], each[-1], each[-11], each[-4]
                 , each[-3], each[-2], each[28], each[29], each[30], each[31]]
    champion_datas = champion_datas[1:]

    rate = []
    for i in range(len(champion_datas)):
        rate.append(calculate_rate(parti_data[i], list(champion_datas[i].values())[0]))   
    train_rate.append(rate)

train_scores = calculate_score(train_rate, positions)
print(train_scores)


"""
Todo:
1. Basic data: Champions that are good at 
done(1). killing tower 
done(2). first blood 
done(3). monster KILLER(baron or dragon) [大龙杀手，小龙杀手，蓝爸爸红爸爸杀手], or 杀敌方野怪[最擅长入侵]最多
(我觉得有连杀数应该就够了)(4). panta kill／。。。
done(5). 最肉tank [take most physical/magic//true demage ]
done(6). 最高输出 (physical/magic/true)
(没找到这个属性) (7). 补兵最多
done(8). 死的最多／存活率[时间]最高
done(9). 助攻王/击杀王
done(10). 控场王[timeCC]
done(11). 最容易连杀
done(12). 死亡频率较高[hidden senior case: 分析死亡数与消极游戏的联系]
done(13). most wards brought/killed (sight/vision) [插言／排眼，是一个好辅助的重要因素之一]
done(14). 最能奶的英雄(heal)
(这个应该没有太大区别？)(15). 红蓝方谁更容易赢
(to do)(16). 推塔数／大龙数[baron]／小龙数[dragon]/峡谷先锋 与比赛输赢的关系
done(17). 暴击王

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

