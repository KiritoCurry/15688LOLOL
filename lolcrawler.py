import sqlite3
import pandas as pd
import math
import time
import random
import traceback
import datetime

import cassiopeia as cass
from cassiopeia import Summoner, Match, Champions
from cassiopeia.data import Season, Queue, Tier

DIAMOND = 10001
PLATINUM = 10001
GOLD = 10001
SLIVER = 10001
BRONZE = 10001
match_error = [0]


def initializeSeed(filename):
    seeds = []
    raw_data = pd.read_csv(filename)
    for idx, data in raw_data.iterrows():
        for sommoner in data:
            seeds.append(sommoner)
    return seeds


def getChampionsItemsAndSpells(conn):
    c = conn.cursor()
    # Get champions, in case the id of champions change because of version change,
    # we sort it first
    champions = Champions(region="NA")
    champion_list = []
    for cham in champions:
        champion_list.append(cham.name)
    champion_list.sort()
    champion2idx = {}
    for i, cham in enumerate(champion_list):
        champion2idx[cham] = i
        c.execute("INSERT INTO Champion VALUES( ?,? )", (i, cham))
    # Get items
    items = cass.get_items(region="NA")
    item_list = []
    for item in items:
        item_list.append(item.name)
    item_list.sort()
    item2idx = {}
    for i, item in enumerate(item_list):
        item2idx[item] = i
        c.execute("INSERT INTO item VALUES(?,?)", (i, item))
    # Get Sommoner Spells
    sspells = cass.get_summoner_spells(region="NA")
    spell_list = []
    for spell in sspells:
        spell_list.append(spell.name)
    spell_list.sort()
    spell2idx = {}
    for i, spell in enumerate(spell_list):
        spell2idx[spell] = i
        c.execute("INSERT INTO summoner_spell VALUES( ?,? )", (i, spell))
    conn.commit()
    return champion2idx, item2idx, spell2idx


def insertSommoner(sommoner, conn, counts):
    c = conn.cursor()
    try:
        league = sommoner.leagues
        # get rank in this season
        if league == None or len(league) == 0 or league.fives == None or len(league.fives) == 0:
            rank_this_season = Tier.unranked.value.lower()
        else:
            rank_this_season = league.fives[0].tier.value.lower()
        # get rank in last season
        rank_last_season = sommoner.rank_last_season.value.lower()
        c.execute("INSERT INTO SUMMONER VALUES(?,?,?,?,?,?,?)",
                  (
                  sommoner.id, sommoner.name, sommoner.region.value, sommoner.level, rank_this_season, rank_last_season,
                  0))
        counts[rank_this_season] += 1
        conn.commit()
    except:
        traceback.print_exc()
        print('Insert Sommner {} failed!'.format(sommoner.name))


def insertMatch(match, conn):
    c = conn.cursor()
    try:
        # Insert the match data first
        c.execute("INSERT INTO MATCH VALUES(?,?,?,?,?,?,?,?,?)", (
        match.id, match.duration.total_seconds(), match.version, match.season.value, match.region.value,
        match.queue.value, match.creation.timestamp, int(match.is_remake), 'unknown'))
        # Then insert 

        conn.commit()
    except:
        traceback.print_exc()
        print('Insert match {} failed!'.format(match.id))


def is_match_duplicate(match, conn):
    try:
        result = pd.read_sql('SELECT * FROM MATCH WHERE id={}'.format(match.id), conn).empty
    except:
        traceback.print_exc()
        print('error during duplicating macth!')
        match_error[0] += 1
        return True
    return not result

    pass


def enough(counts):
    result = True
    for i in counts.values():
        result = result and i > 9999
    return result


def main():
    cass.set_riot_api_key("RGAPI-edcc129f-7b86-44bf-8ced-f3dcbc837886")
    cass.set_default_region("NA")
    """
    1. Initialize seedfiles
    2. Begin crawling
    """
    counts = {}
    counts[Tier.diamond.lower()] = 0
    counts[Tier.platinum.lower()] = 0
    counts[Tier.gold.lower()] = 0
    counts[Tier.silver.lower()] = 0
    counts[Tier.bronze.lower()] = 0
    counts[Tier.unranked.lower()] = 0
    invalid_summon = 0
    total_sommoner = 0
    match_total_num = 0
    match_repeat_num = 0
    match_invalid_num = 0
    match_valid_num = 0

    conn = sqlite3.connect('lol.db')
    unpulled_summoners = initializeSeed('seed.csv')
    # get champion, item, spells maps
    champion2idx, item2idx, spell2idx = getChampionsItemsAndSpells(conn)
    while len(unpulled_summoners) > 0:
        is_enough = False
        random.shuffle(unpulled_summoners)
        for summoner in unpulled_summoners:
            current_summoner = Summoner(name=summoner)
            try:
                # we only need S8 5v5 solo rank data
                allmatches = current_summoner.match_history(seasons={Season.season_8}, queues={Queue.ranked_solo_fives})
                if allmatches == None or len(allmatches) == 0:
                    print('The summoner {} has no matches in {}! Continue.'.format(current_summoner, Season.season_8))
                    invalid_summon += 1
                    continue
            except:
                traceback.print_exc()
                print('The summoner {} not exist!'.format(current_summoner))
                invalid_summon += 1
                continue
            # insert the current summoner into database
            insertSommoner(current_summoner, conn, counts)
            # whether we have got enough data
            if enough(counts):
                is_enough = True
                break
            # begin to visit all matches
            for match in allmatches:
                match_total_num += 1
                # None match, invalid, just skip
                if match == None:
                    print('None match!')
                    match_invalid_num += 1
                    continue
                # Duplicate match, skip
                elif is_match_duplicate(match, conn):
                    match_repeat_num += 1
                    print('match duplicate!')
                    continue
                # This is what we want
                else:
                    match_valid_num += 1
                    # insert match
                    insertMatch(match, conn)
            # update summoner to be already crawled
            c = conn.cursor()
            c.execute("UPDATE Summoner SET is_crawler=1 WHERE id={}".format(current_summoner.id))
            c.commit()

        if is_enough:
            break


if __name__ == '__main__':
    main()
