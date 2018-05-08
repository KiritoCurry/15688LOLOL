
import preprocessing_calculate_score as process
import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('lol.db')
participants = process.get_data(conn, 'Participants')
champions = process.get_data(conn, 'Champion')
ban = process.get_data(conn, 'team_ban')
kill_event = process.get_data(conn, 'kill_champion_event')

# Return two dicts, champion_name & frequency killed by this champion, and champion_name & frequency has ever killed by this champion
# The champion inputted restrain the champion with highest frequency in kills most
# The champion inputted is restrained most by the champion with highest frequency in be_killed_by 
def kill_pairs(champion_id, kill_event, participants, champions):
    kills = {}
    be_killed_by = {}
    matches = []
    ids_inmatch = []
    for p in participants:
        if p[3] == champion_id:
            matches.append(p[2])
            ids_inmatch.append(p[0])

    killer_id_inmatch = {}
    killed_id_inmatch = {}
    for i in range(len(matches)):
        for k in kill_event:
            if int(k[1]) == matches[i] and k[2] == ids_inmatch[i]:
                if matches[i] in killer_id_inmatch:
                    killer_id_inmatch[matches[i]].append(k[3])
                else:
                    killer_id_inmatch[matches[i]] = []
                    killer_id_inmatch[matches[i]].append(k[3])
            if int(k[1]) == matches[i] and k[3] == ids_inmatch[i]:
                if matches[i] in killed_id_inmatch:
                    killed_id_inmatch[matches[i]].append(k[2])
                else:
                    killed_id_inmatch[matches[i]] = []
                    killed_id_inmatch[matches[i]].append(k[2])
    
    for each in killer_id_inmatch:
        for k in killer_id_inmatch[each]:
            for p in participants:
                if p[2] == each:
                    if p[0] == k:
                        champion_name = champions[p[3]][1]
                        if champion_name in be_killed_by:
                            be_killed_by[champion_name] += 1
                        else:
                            be_kbe_killed_byilled[champion_name] = 1

    for each in killed_id_inmatch:
        for k in kilkilled_id_inmatchled[each]:
            for p in participants:
                if p[2] == each:
                    if p[0] == k:
                        champion_name = champions[p[3]][1]
                        if champion_name in kills:
                            kills[champion_name] += 1
                        else:
                            kills[champion_name] = 1
    
    
    return kills, be_killed_by

# Main function

kills, be_killed_by = kill_pairs(55, kill_event, participants, champions)
restrain_most = max(kills.items(), key=lambda x: x[1])
be_restrained_most = max(be_killed_by.items(), key=lambda x: x[1])
print(restrain_most, be_restrained_most)

    

