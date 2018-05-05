import sqlite3
import pandas as pd
import math
import time
import random
import traceback
import datetime
import json
from collections import Counter

import cassiopeia as cass
from cassiopeia import Summoner, Match, Champions, Champion
from cassiopeia.data import Season, Queue, Tier

DIAMOND = 10001
PLATINUM = 10001
GOLD = 10001
SLIVER = 10001
BRONZE = 10001
match_error = [0]


def is_resume(conn):
    try:
        result = pd.read_sql('SELECT * FROM Champion', conn).empty
    except:
        traceback.print_exc()
        print('Cannot resume!')
        return
    return not result

def resume_dicts(conn):
    champions=list(pd.read_sql("SELECT name from Champion", conn)['name'])
    champion2idx={}
    for i,c in enumerate(champions):
        champion2idx[c]=i

    items=list(pd.read_sql("SELECT name from item", conn)['name'])
    item2idx = {}
    for i, item in enumerate(items):
        item2idx[item] = i

    spells=list(pd.read_sql("SELECT name from summoner_spell", conn)['name'])
    spell2idx = {}
    for i, spell in enumerate(spells):
        spell2idx[spell] = i
    return champion2idx,item2idx,spell2idx

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


def is_summoner_duplicate(summoner, conn):
    try:
        result = pd.read_sql('SELECT * FROM Summoner WHERE id={}'.format(summoner.id), conn).empty
    except:
        traceback.print_exc()
        print('error during duplicating summoner!')
        return True

    return not result


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
                      sommoner.id, sommoner.name, sommoner.region.value, sommoner.level, rank_this_season,
                      rank_last_season,
                      0))
        counts[rank_this_season] += 1
        conn.commit()
    except:
        traceback.print_exc()
        print('Insert Sommner {} failed!'.format(sommoner.name))


def insertMatch(match, conn, champion2idx, item2idx, spell2idx):
    c = conn.cursor()
    try:
        # Insert the match data first
        c.execute("INSERT INTO MATCH VALUES(?,?,?,?,?,?,?,?,?)", (
            match.id, match.duration.total_seconds(), match.version, match.season.value, match.region.value,
            match.queue.value, match.creation.timestamp, int(match.is_remake), 'unknown'))
        # insert teams info
        insertTeams(conn, match)
        # insert team ban info
        insertTeamBan(match, conn, champion2idx)
        # Then insert participants
        participants = match.participants
        for p in participants:
            # insert every participant with its stats
            insertParticipant(p, conn, champion2idx, item2idx, spell2idx, match)
            # insert participant timeline
            insertParticipantTimeline(p, conn, match)

        # After inserting participant, calculate the match's rank by selecting the most common one
        # among 10 participants
        try:
            ranks = list(pd.read_sql(
                "select rank_this_season from Summoner where Summoner.id in (select summoner_id from Participants where match_id={})".format(
                    match.id), conn)['rank_this_season'])
            match_rank=Counter(ranks)
            match_rank=match_rank.most_common(1)[0][0]
            print('match {} has average tier of {}.'.format(match.id,match_rank))
            c.execute("UPDATE match SET tier = ? where id=?",(match_rank,match.id))
        except:
            traceback.print_exc()
            print('error when updating match {} tier!'.format(match.id))

        if match.timeline == None or match.timeline.frames == None:
            print('This match{} does no have events!'.format(match.id))
            return
        else:
            for frame in match.timeline.frames:
                events = frame.events
                # insert kill champion and kill monster event
                insertEvent(events, conn, match)
        conn.commit()
    except:
        traceback.print_exc()
        print('Insert match {} failed!'.format(match.id))


def insertEvent(events, conn, match):
    c = conn.cursor()
    try:
        for event in events:
            if event == None:
                continue
            elif event.type == 'CHAMPION_KILL' and event.victim_id != None and event.killer_id != None:
                c.execute(
                    'INSERT INTO kill_champion_event (match_id,victim_id,killer_id, happen_time) VALUES (?,?,?,?)',
                    (match.id, event.victim_id, event.killer_id, event.timestamp))
            elif event.type == 'ELITE_MONSTER_KILL' and event.monster_type != None and event.killer_id != None:
                c.execute('INSERT INTO kill_monster_event (match_id,timestamp,killer_id,monster_type) VALUES (?,?,?,?)',
                          (match.id, event.timestamp, event.killer_id, event.monster_type))
        conn.commit()
    except:
        traceback.print_exc()
        print('Event error in match{} !'.format(match.id))

    pass


def is_match_duplicate(match, conn):
    try:
        result = pd.read_sql('SELECT * FROM MATCH WHERE id={}'.format(match.id), conn).empty
    except:
        traceback.print_exc()
        print('error during duplicating macth!')
        match_error[0] += 1
        return True
    return not result


"""
Blue team id=1
read tema id=2
"""


def insertTeams(conn, match):
    c = conn.cursor()
    try:
        # Insert the blue team
        blueteam = match.blue_team
        c.execute("INSERT INTO Team VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            1, match.id, 'blue', int(blueteam.win), blueteam.dragon_kills, blueteam.baron_kills,
            blueteam.inhibitor_kills, blueteam.tower_kills, blueteam.first_blood, blueteam.first_dragon,
            blueteam.first_baron, blueteam.first_tower, blueteam.first_rift_herald))
        # Insert red team
        redteam = match.red_team
        c.execute("INSERT INTO Team VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            2, match.id, 'red', int(redteam.win), redteam.dragon_kills, redteam.baron_kills,
            redteam.inhibitor_kills, redteam.tower_kills, redteam.first_blood, redteam.first_dragon,
            redteam.first_baron, redteam.first_tower, redteam.first_rift_herald))
        conn.commit()
    except:
        traceback.print_exc()
        print('Insert match {} Team failed!'.format(match.id))


def insertTeamBan(match, conn, champion2idx):
    c = conn.cursor()
    try:
        # blue team ban
        blueteam = match.blue_team
        blue_bans = blueteam.bans
        for bb in blue_bans:
            if bb != None:
                champion = Champion(id=bb.id)
                c.execute("INSERT INTO team_ban (team_id,match_id,ban_champion) VALUES (?,?,?)",
                          (1, match.id, champion2idx[champion.name]))
        # red team ban
        redteam = match.red_team
        red_bans = redteam.bans
        for rb in red_bans:
            if rb != None:
                champion = Champion(id=rb.id)
                c.execute("INSERT INTO team_ban (team_id,match_id,ban_champion) VALUES (?,?,?)",
                          (2, match.id, champion2idx[champion.name]))
        conn.commit()
    except:
        traceback.print_exc()
        print('Insert Match {} Team ban failed!'.format(match.id))


def insertParticipantTimeline(participant, conn, match):
    c = conn.cursor()
    try:
        timeline = participant.timeline
        creeps_per_min_deltas = json.dumps(timeline.creeps_per_min_deltas)
        cs_diff_per_min_deltas = json.dumps(timeline.cs_diff_per_min_deltas)
        damage_taken_diff_per_min_deltas = json.dumps(timeline.damage_taken_diff_per_min_deltas)
        gold_per_min_deltas = json.dumps(timeline.gold_per_min_deltas)
        damage_taken_per_min_deltas = json.dumps(timeline.damage_taken_per_min_deltas)
        xp_diff_per_min_deltas = json.dumps(timeline.xp_diff_per_min_deltas)
        xp_per_min_deltas = json.dumps(timeline.xp_per_min_deltas)
        c.execute("INSERT INTO participant_timeline VALUES (?,?,?,?,?,?,?,?,?,?)", (
            participant.id, participant.summoner.id, match.id, creeps_per_min_deltas, cs_diff_per_min_deltas,
            damage_taken_diff_per_min_deltas, gold_per_min_deltas, damage_taken_per_min_deltas, xp_diff_per_min_deltas,
            xp_per_min_deltas))
        conn.commit()
    except:
        traceback.print_exc()
        print('Insert Participant {} {}timeline info failed!'.format(participant.summoner.name, match.id))


def insertParticipant(participant, conn, champion2idx, counts, spell2idx, match):
    c = conn.cursor()
    try:
        summoner = participant.summoner
        # insert this summoer if it's not included before
        if not is_summoner_duplicate(summoner, conn):
            insertSommoner(summoner, conn, counts)
        stats = participant.stats
        pid = participant.id
        summoner_id = summoner.id
        match_id = match.id
        champion_id = champion2idx[participant.champion.name]
        side = participant.side.name
        win = participant.team.win
        role = participant.role
        if role != None and type(role) != str:
            role = role.value
        try:
            lane = participant.lane.value
        except:
            lane=None
        sspell1 = spell2idx[participant.summoner_spell_d.name]
        sspell2 = spell2idx[participant.summoner_spell_f.name]
        level = stats.level
        items = []
        for it in stats.items:
            if it != None:
                items.append(it.name)
        items = ",".join(items)
        kills = stats.kills
        deaths = stats.deaths
        assist = stats.assists
        kda = stats.kda
        turret_kills = stats.turret_kills
        first_tower_kill = int(stats.first_tower_kill)
        damage_dealt_to_turrets = stats.damage_dealt_to_turrets
        first_blood_kill = int(stats.first_blood_kill)
        double_kills = stats.double_kills
        triple_kills = stats.triple_kills
        quadra_kills = stats.quadra_kills
        penta_kills = stats.penta_kills
        killing_sprees = stats.killing_sprees
        inhibitor_kills = stats.inhibitor_kills
        gold_earned = stats.gold_earned
        gold_spent = stats.gold_spent
        largest_killing_spree = stats.largest_killing_spree
        largest_critical_strike = stats.largest_critical_strike
        largest_multi_kill = stats.largest_multi_kill
        longest_time_spent_living = stats.longest_time_spent_living
        magic_damage_dealt_to_champions = stats.magic_damage_dealt_to_champions
        magical_damage_taken = stats.magical_damage_taken
        neutral_minions_killed = stats.neutral_minions_killed
        neutral_minions_killed_enemy_jungle = stats.neutral_minions_killed_enemy_jungle
        physical_damage_dealt_to_champions = stats.physical_damage_dealt_to_champions
        physical_damage_taken = stats.physical_damage_taken
        sight_wards_bought_in_game = stats.sight_wards_bought_in_game
        total_damage_dealt_to_champions = stats.total_damage_dealt_to_champions
        total_damage_taken = stats.total_damage_taken
        total_heal = stats.total_heal
        total_minions_killed = stats.total_minions_killed
        true_damage_dealt_to_champions = stats.true_damage_dealt_to_champions
        true_damage_taken = stats.true_damage_taken
        vision_wards_bought_in_game = stats.vision_wards_bought_in_game
        wards_killed = stats.wards_killed
        wards_placed = stats.wards_placed
        time_CCing_others = stats.time_CCing_others

        c.execute(
            "INSERT INTO Participants VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                pid, summoner_id, match_id, champion_id, side, win, role, lane, sspell1, sspell2, level, items, kills,
                deaths,
                assist,
                kda, turret_kills, first_tower_kill, damage_dealt_to_turrets, first_blood_kill, double_kills,
                triple_kills,
                quadra_kills, penta_kills, killing_sprees, inhibitor_kills, gold_earned, gold_spent,
                largest_killing_spree, largest_critical_strike, largest_multi_kill, longest_time_spent_living,
                magic_damage_dealt_to_champions, magical_damage_taken, neutral_minions_killed,
                neutral_minions_killed_enemy_jungle, physical_damage_dealt_to_champions, physical_damage_taken,
                sight_wards_bought_in_game, total_damage_dealt_to_champions, total_damage_taken, total_heal,
                total_minions_killed, true_damage_dealt_to_champions, true_damage_taken, vision_wards_bought_in_game,
                wards_killed, wards_placed, time_CCing_others))
        conn.commit()
    except:
        traceback.print_exc()
        print('Insert Participant {} , {}, {} failed!'.format(participant.id, participant.champion.name,
                                                              participant.role))


def enough(counts):
    result = True
    for i in counts.values():
        result = result and i > 9999
    return result


def main():
    cass.set_riot_api_key("RGAPI-fc286f72-6f80-46c3-90ae-2de6d30f6463")
    cass.set_default_region("NA")
    conn = sqlite3.connect('lol.db')
    counts = {}
    counts[Tier.diamond.value.lower()] = 0
    counts[Tier.platinum.value.lower()] = 0
    counts[Tier.gold.value.lower()] = 0
    counts[Tier.silver.value.lower()] = 0
    counts[Tier.bronze.value.lower()] = 0
    counts[Tier.unranked.value.lower()] = 0
    invalid_summon = 0
    total_sommoner = 0
    match_total_num = 0
    match_repeat_num = 0
    match_invalid_num = 0
    match_valid_num = 0

    is_seed=True
    """
    1. Initialize seedfiles
    2. Begin crawling
    """
    if is_resume(conn):
        print('Crawler resume. Count Restart.')
        unpulled_summoners = list(pd.read_sql("SELECT name from Summoner where is_crawler=0", conn)['name'])
        champion2idx, item2idx, spell2idx=resume_dicts(conn)
    else:
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
            print('Begin crawl Summoner {}, he has {} matches in S8.'.format(current_summoner.name, len(allmatches)))
            # insert the current summoner into database if this is first loop
            if is_seed and not is_summoner_duplicate(current_summoner,conn):
                insertSommoner(current_summoner, conn, counts)
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
                    insertMatch(match, conn, champion2idx, counts, spell2idx)
                    # whether we have got enough data
            # update summoner to be already crawled
            c = conn.cursor()
            c.execute("UPDATE Summoner SET is_crawler=1 WHERE id={}".format(current_summoner.id))
            conn.commit()
            if enough(counts):
                is_enough = True
                break
        if is_enough:
            break
        is_seed=False
        unpulled_summoners = list(pd.read_sql("SELECT name from Summoner where is_crawler=0", conn)['name'])

    print('Finish crawling!')
    print(
        'We have crawled {} summoners in total,{} diamond, {} platinum, {} gold, {} silver, {} bronze, {} unranked.'.format(
            sum(counts.values()), counts['diamond'], counts['platinum'], counts['gold'], counts['silver'],
            counts['bronze'], counts['unranked']))
    print('We have crawled {} matches in total, {} error match, {} duplicate match, {} normal match'.format(
        match_total_num, match_invalid_num + match_error[0], match_repeat_num - match_error[0], match_valid_num))
    conn.close()


if __name__ == '__main__':
    main()
