import preprocessing_calculate_score as process
import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('lol.db')
participants = process.get_data(conn, 'Participants')
champions = process.get_data(conn, 'Champion')

# Get all teammates this champion has ever grouped with, and this champion's performance of those matches
# Team_mates & match_performance are corresponding, match_id is the first element of match_performance
# Different positions have different evalutation of performance. Here consider minions number for JUNGLE, wards number
# SUPPORT
def get_teammate_and_performance(champion_id, position, participants, champions):
    data = []
    team_mates = []
    
    for p in participants:
        if p[3] == champion_id:
            if p[6] == position or p[7] == position:
                match = []
                match.extend([p[2], p[4], p[5], p[15], p[39], p[48]])
                if position == 'DUO_SUPPORT':
                    match.extend([(p[38]+p[45]+p[46]+p[47]), 0])
                elif position == 'JUNGLE':
                    match.extend([0, (p[34]+p[35])])
                else:
                    match.extend([0, 0])
                data.append(match)

    for d in data:
        team = []
        for p in participants:
            if p[2] == d[0] and p[4] == d[1]:
                if p[3] != champion_id:
                    pos = process.get_position(p)
                    team.append([pos,p[3]])
        
        team_mates.append(team)
    match_performance = [([d[0]]+d[2:]) for d in data]
    return team_mates, match_performance

# Normalize all data into range 0-5
def normalize(data):
    norms = []
    maxi = max(data)
    mini = min(data)
    unit = (maxi - mini)/5
    for d in data:
        l = (d-mini)/unit
        norms.append(l)
    return norms

# Get top three teams with highest normalized performance 
def top_three(l, teammates):
    m = {}
    for a in l:
        if a in m:
            m[a].append(l.index(a))
        else:
            m[a] = [l.index(a)]
    l = sorted(l, reverse=True)
    index = l[0:3]
    res = []
    for i in [m[i] for i in index]:
        for j in i:
            res.append(teammates[j])
            
    return res
    
# Normalize each performance criteria and add them together, select best team according to the normalized total performance 
def best_performance_group(data, position, teammates):
    wins = [d[0] for d in data]
    kda = [d[1] for d in data]
    total_damage_to = [d[2] for d in data]
    time_CCing = [d[3] for d in data]
    wards = [d[4] for d in data]
    minions = [d[5] for d in data] 
    norms = []
    average = []

    if position == 'DUO_SUPPORT':
        norms.extend([normalize(wins), normalize(kda), normalize(total_damage_to),
                       normalize(time_CCing),normalize(wards)])
        for i in range(len(wins)):
            average.append((wins[i]+kda[i]+total_damage_to[i]+time_CCing[i]+wards[i])/5)
        return top_three(average, teammates)
        
    
    elif position == 'JUNGLE':
        norms.extend([normalize(wins), normalize(kda), normalize(total_damage_to),
                       normalize(time_CCing),normalize(minions)])
        for i in range(len(wins)):
            average.append((wins[i]+kda[i]+total_damage_to[i]+time_CCing[i]+minions[i])/5)
        return top_three(average, teammates)
    
    else:
        norms.extend([normalize(wins), normalize(kda), normalize(total_damage_to),
                       normalize(time_CCing)])
        for i in range(len(wins)):
            average.append((wins[i]+kda[i]+total_damage_to[i]+time_CCing[i])/4)
        return top_three(average, teammates)

teammates, performance_data = get_teammate_and_performance(0, 'TOP_LANE', participants, champions)
best_group = best_performance_group(performance_data, 'TOP_LANE', teammates)
print(best_group)

