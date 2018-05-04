import sqlite3
import pandas as pd
import math
import time
import random

import cassiopeia as cass
from cassiopeia import Summoner, Match, Champions
from cassiopeia.data import Season, Queue

DIAMOND=10001
PLATINUM=10001
GOLD=10001
SLIVER=10001
BRONZE=10001

def initializeSeed(filename):
    seeds=[]
    raw_data=pd.read_csv(filename)
    for idx,data in raw_data.iterrows():
        for sommoner in data:
            seeds.append(sommoner)
    return seeds

def getChampionsItemsAndSpells(conn):
    c = conn.cursor()
    # Get champions, in case the id of champions change because of version change,
    # we sort it first
    champions = Champions(region="NA")
    champion_list=[]
    for cham in champions:
        champion_list.append(cham.name)
    champion_list.sort()
    champion2idx={}
    for i,cham in enumerate(champion_list):
        champion2idx[cham]=i
        c.execute("INSERT INTO Champion VALUES( ?,? )",(i,cham))
    # Get items
    items = cass.get_items(region="NA")
    item_list=[]
    for item in items:
        item_list.append(item.name)
    item_list.sort()
    item2idx={}
    for i,item in enumerate(item_list):
        item2idx[item]=i
        c.execute("INSERT INTO item VALUES(?,?)",(i,item))
    # Get Sommoner Spells
    sspells = cass.get_summoner_spells(region="NA")
    spell_list=[]
    for spell in sspells:
        spell_list.append(spell.name)
    spell_list.sort()
    spell2idx={}
    for i,spell in enumerate(spell_list):
        spell2idx[spell]=i
        c.execute("INSERT INTO summoner_spell VALUES( ?,? )",(i, spell))
    conn.commit()
    return champion2idx,item2idx,spell2idx







def main():
    cass.set_riot_api_key("RGAPI-edcc129f-7b86-44bf-8ced-f3dcbc837886")
    cass.set_default_region("NA")
    """
    1. Initialize seedfiles
    2. Begin crawling
    """
    diamond_count=0
    platinum_count=0
    gold_count=0
    sliver_count=0
    bronze_count=0
    nonrank_count=0
    total_sommoner=0
    match_total_num=0
    match_repeat_num=0
    match_invalid_num=0


    conn = sqlite3.connect('lol.db')
    unpulled_summoners=initializeSeed('seed.csv')
    # get champion, item, spells maps
    champion2idx,item2idx,spell2idx=getChampionsItemsAndSpells(conn)
    while len(unpulled_summoners)>0:
        is_enough=False
        random.shuffle(unpulled_summoners)
        for summoner in unpulled_summoners:
            current_summoner=Summoner(name=summoner)

        # whether we have got enough data
        if diamond_count<DIAMOND or platinum_count<PLATINUM or gold_count<GOLD or sliver_count<SLIVER or bronze_count<BRONZE:
            is_enough=True
            break

    pass





if __name__=='__main__':
    main()
