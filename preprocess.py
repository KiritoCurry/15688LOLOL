import sqlite3
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.linear_model import BayesianRidge
from sklearn.preprocessing import StandardScaler, MinMaxScaler

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
                    physical_damage_to[pos].append(p[-9])
                    physical_damage_taken[pos].append(p[-8])
                    magic_damage_to[pos].append(p[-13])
                    magic_damage_taken[pos].append(p[-12])
                    true_damage_to[pos].append(p[-6])
                    true_damage_taken[pos].append(p[-5])
                    gold_earned[pos].append(p[26])
                    gold_spent[pos].append(p[27])
                    tower_kill[pos].append(p[16])
                    minions_kill[pos].append(p[-11])
                    minions_kill_enemy[pos].append(p[-10])
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


def predict_lane():
    for i, champion_data in enumerate(all_data):
        best_rate = 0.0
        best_lane = ""
        for lane in champion_data.keys():
            win_rate = champion_data[lane][1]['win_rate']
            if win_rate > best_rate:
                best_rate = win_rate
                best_lane = lane
        all_data[i]['lane_with_best_win_rate'] = lane
    return


def get_match_data(match, participants):
    # kda, gold, kill
    match_data = []
    for m in match:
        match_id = m[0]
        curr_match = {'red':{'kills':0, 'kda': 0, 'income':0}, 'blue':{'kills':0, 'kda': 0, 'income':0}}
        
        win = ''
        for p in participants:
            if p[2] == match_id:
                curr_match[p[4]]['kills'] += p[12]
                curr_match[p[4]]['kda'] += p[15]
                curr_match[p[4]]['income'] += p[26]
                curr_match[p[4]]['income'] -= p[27]
                
                if p[5] == 1:
                    win = p[4]
                    
        curr_match['win_side'] = win
        match_data.append(curr_match)
    
    return match_data
        
def predict_result(match_id, match_data, verbose=False):
    X = []
    y = []
    for i, match in enumerate(match_data):
        X.append([])
        # Avoid division by zero
        X[i].append(match['red']['kda'] / (match['blue']['kda'] + 1e-6))
        X[i].append(match['red']['income'] / (match['blue']['income'] + 1e-6))
        X[i].append(match['red']['kills'] / (match['blue']['kills'] + 1e-6))
        
        if match['win_side'] == 'red':
            y.append(0)
        else:
            y.append(1)
   
    scaler = MinMaxScaler()
    clf = svm.SVC(C=1e10, max_iter=50, kernel='linear')
    # clf = BayesianRidge(compute_score=True)
    X = np.array(X)
    y = np.array(y)
    scaler.fit(X)
    X_train = scaler.transform(X)
    clf.fit(X_train, y)
    if verbose:
        ret = clf.predict(X_train)
        tot = len(ret)
        hit = 0
        for pred, true in zip(ret, y):
            if pred == true:
                hit += 1
        print("train_accuracy:{:.3f}".format(hit/tot))
    
    ret = clf.predict(X_train[match_id].reshape([1,-1]))
    return 'red' if ret == 0 else 'blue'

participants = get_data(conn, 'Participants')
champion = get_data(conn, 'Champion')
ban = get_data(conn, 'team_ban')
kill_monster_event = get_data(conn, 'kill_monster_event')
match = get_data(conn, 'Match')

all_data = []

for c in champion:
    all_data.append(champion_data(c[0], participants))

predict_lane()
match_data = get_match_data(match, participants)

predict_result(0, match_data, verbose=True)