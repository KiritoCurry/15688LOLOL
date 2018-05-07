
# coding: utf-8

# In[27]:


import preprocessing_calculate_score as process
import sqlite3
import pandas as pd
import numpy as np


# In[42]:


conn = sqlite3.connect('lol.db')
participants = process.get_data(conn, 'Participants')
champions = process.get_data(conn, 'Champion')
ban = process.get_data(conn, 'team_ban')
kill_event = process.get_data(conn, 'kill_champion_event')


# In[44]:


def kill_pairs(champion_id, kill_event, participants, champions):
    kills = {}
    be_killed = {}
    matches = []
    ids = []
    for p in participants:
        if p[3] == champion_id:
            matches.append(p[2])
            ids.append(p[0])

    killer = {}
    killed = {}
    for i in range(len(matches)):
        for k in kill_event:
            if int(k[1]) == matches[i] and k[2] == ids[i]:
                if matches[i] in killer:
                    killer[matches[i]].append(k[3])
                else:
                    killer[matches[i]] = []
                    killer[matches[i]].append(k[3])
            if int(k[1]) == matches[i] and k[3] == ids[i]:
                if matches[i] in killed:
                    killed[matches[i]].append(k[2])
                else:
                    killed[matches[i]] = []
                    killed[matches[i]].append(k[2])
    
    for each in killer:
        for k in killer[each]:
            for p in participants:
                if p[2] == each:
                    if p[0] == k:
                        champion_name = champions[p[3]][1]
                        if champion_name in be_killed:
                            be_killed[champion_name] += 1
                        else:
                            be_killed[champion_name] = 1

    for each in killed:
        for k in killed[each]:
            for p in participants:
                if p[2] == each:
                    if p[0] == k:
                        champion_name = champions[p[3]][1]
                        if champion_name in kills:
                            kills[champion_name] += 1
                        else:
                            kills[champion_name] = 1
    
    
    return kills, be_killed


    


# In[45]:


kills, be_killed = kill_pairs(55, kill_event, participants, champions)
most_restrain = max(kills.items(), key=lambda x: x[1])
be_restrained = max(be_killed.items(), key=lambda x: x[1])
print(most_restrain, be_restrained)

    

