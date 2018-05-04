import sqlite3
import pandas as pd
import math
import time
import random

import cassiopeia as cass
from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue

DIAMOND=10001
PLATINUM=10001
GOLD=10001
SLIVER=10001
BRONZE=10001

def initializeSeed(filename):
    seeds=pd.read_csv(filename)
    
    pass





def main():
    cass.set_riot_api_key("RGAPI-edcc129f-7b86-44bf-8ced-f3dcbc837886")
    cass.set_default_region("NA")
    """
    1. Initialize seedfiles
    2. Begin crawling
    """
    diamond_count=10
    platinum_count=10
    gold_count=10
    sliver_count=10
    bronze_count=10
    print('')
    unpulled_summoners=initializeSeed('seed.csv')
    while len(unpulled_summoners)>0:
        if diamond_count<DIAMOND or platinum_count<PLATINUM or gold_count<GOLD or sliver_count<SLIVER or bronze_count<BRONZE:
            break

    pass





if __name__=='__main__':

    main()