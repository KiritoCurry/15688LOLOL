import sqlite3
import pandas as pd
import numpy as np


conn = sqlite3.connect('lol.db')
def get_data(conn, table_name):
    res = []
    query = 'SELECT * FROM ' + table_name
    c = conn.cursor()
    data = c.execute(query)
    for d in data:
        res.append(d)
    return res

# get a participant's position
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

# Get all useful average data for a champion
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
                    chosen_rate[pos] = 0
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

# 从这里开始是calculate_summoner_score section

# Calculate the rate of difference bewteen summoner performance and average performance, divided by the summoner performance
# 就是看玩家的表现超出/少于平均值 是他自己表现的多少倍
def performance_rate(data, average):
    if data == 0:
        return 0
    return (data-average)/data

# Calulate the relative score for each participant according to their position
# data_set: the performance rate calculated for each participant
# position: used to decide different weights
def calculate_score(data_set, position):
    train_scores = []
    sums = []
    jungle = []
    top = []
    mid = []
    adc = []
    support = []
    duo=[]
    
    # 按顺序0-25:
    # 0.win_rate
    # 1.kills
    # 2.deaths
    # 3.assists
    # 4. physical_damage_to
    # 5. physical_damage_taken
    # 6. magic_damage_to
    # 7. magic_damage_taken
    # 8. true_damage_to
    # 9. true_damage_taken
    # 10. gold_earned
    # 11. gold_spent
    # 12. tower_kill
    # 13. minions_kill
    # 14. minions_kill_enemy
    # 15. first_blood
    # 16. total_heal
    # 17. time_CCing
    # 18. sight_ward
    # 19. vision_ward
    # 20. wards_killed
    # 21. wards_placed
    # 22. largest_killing_spree
    # 23. largest_critical_strike
    # 24. largest_multi_kill
    # 25. longest_living_time
    # gold_earned(d[10])没有计入评分，只考虑了gold_spent(d[11])

    for i in range(len(data_set)):
        d = data_set[i]
        try:
            # This is actually DUO, use this as default for others, all weights are among the least ones in all positions
            if position[i]==None:
                s = 30 * d[0] + 20 * d[1] - 23 * d[2] + 10 * d[3] + 10 * (d[4] + d[6] + d[8]) - 2 * (
                        d[5] + d[7] + d[9])
                +4 * d[10] + d[11] / d[10] + 10 * d[12] + 5 * d[13] + 4 * d[14] + 3 * d[15] + 2 * d[16] + 20 * d[17]
                +3 * (d[18] + d[19] + d[20] + d[21]) + 5 * d[22] + 5 * d[23] + 3 * d[24] + 5 * d[25]
                sums.append(s)
                duo.append(s)

            elif position[i] == 'JUNGLE':
                s = 30*d[0]+28*d[1]-20*d[2]+25*d[3]+28*(d[4]+d[6]+d[8])+ 15*(d[5]+d[7]+d[9])
                +5*d[10]+d[11]/d[10]+10*d[12]+ 15*d[13]+40*d[14]+6*d[15]+2*d[16]+20*d[17]
                +15*(d[18]+d[19]+d[20]+d[21])+10*d[22]+15*d[23]+5*d[24]+10*d[25]
                sums.append(s)
                jungle.append(s)

            elif position[i] == 'TOP_LANE':
                s = 30*d[0]+30*d[1]-23*d[2]+15*d[3] + 30*(d[4]+d[6]+d[8]) + 17*(d[5]+d[7]+d[9])
                +6*d[10]+d[11]/d[10] + 10*d[12]+10*d[13]+8*d[14] +6*d[15]+2*d[16]+20*d[17]
                +5*(d[18]+d[19]+d[20]+d[21])+15*d[22]+20*d[23]+5*d[24]+10*d[25]
                sums.append(s)
                top.append(s)

            elif position[i] == 'MID_LANE':
                s = 30*d[0]+30*d[1]-23*d[2]+20*d[3] + 30*(d[4]+d[6]+d[8])+ 5*(d[5]+d[7]+d[9])
                +6*d[10]+d[11]/d[10] + 10*d[12]+10*d[13]+8*d[14] +6*d[15]+2*d[16]+30*d[17]
                +10*(d[18]+d[19]+d[20]+d[21])+15*d[22]+20*d[23]+5*d[24]+15*d[25]
                sums.append(s)
                mid.append(s)

            elif position[i] == 'DUO_CARRY':
                s = 30*d[0]+30*d[1]-23*d[2]+10*d[3]+30*(d[4]+d[6]+d[8])-2*(d[5]+d[7]+d[9])
                +6*d[10]+d[11]/d[10] + 10*d[12]+10*d[13]+6*d[14] +6*d[15]+d[16]+20*d[17]
                +3*(d[18]+d[19]+d[20]+d[21])+15*d[22]+20*d[23]+5*d[24]+20*d[25]
                sums.append(s)
                adc.append(s)

            elif position[i] == 'DUO_SUPPORT':
                s = 30*d[0]+20*d[1]-15*d[2]+30*d[3]+10*(d[4]+d[6]+d[8])+ 20*(d[5]+d[7]+d[9])
                +4*d[10]+d[11]/d[10] + 10*d[12]+5*d[13]+4*d[14] +3*d[15]+15*d[16]+30*d[17]
                +30*(d[18]+d[19]+d[20]+d[21])+5*d[22]+5*d[23]+3*d[24]+5*d[25]
                sums.append(s)
                support.append(s)
            else:
                sums.append('unknown')
        except TypeError:
            sums.append('unknown')
            
    jungle_max = max(jungle)
    jungle_min = min(jungle)
    top_max = max(top)
    top_min = min(top)
    mid_max = max(mid)
    mid_min = min(mid)
    adc_max = max(adc)
    adc_min = min(adc)
    support_max = max(support)
    support_min = min(support)
    duo_max=max(duo)
    duo_min=min(duo)
    
    for i in range(len(sums)):
        if sums[i] != 'unknown':
            if position[i] ==None:
                unit = 98 / (duo_max - duo_min)
                train_scores.append((sums[i] - duo_min) * unit + 1)
            elif position[i] == 'JUNGLE':
                unit = 98/(jungle_max-jungle_min)
                train_scores.append((sums[i]-jungle_min)*unit + 1)
            elif position[i] == 'TOP_LANE':
                unit = 98/(top_max-top_min)
                train_scores.append((sums[i]-top_min)*unit + 1)
            elif position[i] == 'MID_LANE':
                unit = 98/(mid_max-mid_min)
                train_scores.append((sums[i]-mid_min)*unit + 1)
            elif position[i] == 'DUO_CARRY':
                unit = 98/(adc_max-adc_min)
                train_scores.append((sums[i]-adc_min)*unit + 1)
            elif position[i] == 'DUO_SUPPORT':
                unit = 98/(support_max-support_min)
                train_scores.append((sums[i]-support_min)*unit + 1)
            else:
                train_scores.append(0)
        else:
            train_scores.append(0)
    return train_scores    


# Main 方法
# participants = get_data(conn, 'Participants')
# champion = get_data(conn, 'Champion')
# ban = get_data(conn, 'team_ban')
# 
# print(champion)
# all_champion_datas = []
# for c in champion:
#     all_champion_datas.append(champion_data(c[0], participants))
# for i,d in enumerate(all_champion_datas):
# 
#     if 'JUNGLE' in d:
#         print(champion[i][1],d['JUNGLE'][1]['win_rate'],d['JUNGLE'][0]['chosen_rate'])
#     else:
#         print(champion[i][1],'no junngel data!')
# print(len(all_champion_datas),all_champion_datas)
# print(len(all_champion_datas[0]['JUNGLE']))
# parti_performance_rate = []
# positions = []
# 
# 
# for each in train[0:1000]:
#     this_champion_data = all_champion_datas[each[3]]
#     # ‘TOP' 'MID' 'JUNGLE'
#     if each[6] in this_champion_data:
#         this_champion_data = this_champion_data[each[6]]
#         positions.append(each[6])
#     # 'adc' 'support'
#     elif each[7] in this_champion_data:
#         this_champion_data = this_champion_data[each[7]]
#         positions.append(each[7])
#     else:
#         # 现有数据里，这个英雄没有打过这个位置，所以没有平均值，无法评分
#         parti_performance_rate.append(0)
#         positions.append(each[6])
#         continue
# 
#     # 按顺序: win_rate, kills, deaths, assists, physical_damage_to, physical_damage_taken, magic_damage_to, magic_damage_taken, true_damage_to,
#     # true_damage_taken, gold_earned, gold_spent, tower_kill, minions_kill, minions_kill_enemy, first_blood, total_heal,
#     # time_CCing, sight_ward, vision_ward, wards_killed, wards_placed, largest_killing_spree, largest_critical_strike,
#     # largest_multi_kill, longest_living_time
#     parti_data = [each[5], each[12], each[13], each[14], each[-9], each[-8], each[-13], each[-12], each[-6], each[-5],
#                  each[26], each[27], each[16], each[-11], each[-10], each[19], each[-8], each[-1], each[-11], each[-4]
#                  , each[-3], each[-2], each[28], each[29], each[30], each[31]]
#     this_champion_data = this_champion_data[1:]
# 
#     rate_for_one_parti = []
#     for i in range(len(this_champion_data)):
#         rate_for_each.append(performance_rate(parti_data[i], list(this_champion_data[i].values())[0]))
#     parti_performance_rate.append(rate_for_each)
# 
# summoner_scores = calculate_score(parti_performance_rate, positions)
# print(train_scores)

from sklearn.svm import SVC
# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()
# scaler.fit(X)
# X_train = scaler.transform(X)


# In[ ]:


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

