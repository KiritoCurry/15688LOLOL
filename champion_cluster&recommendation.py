from preprocessing_calculate_score import *
from sklearn.cluster import AgglomerativeClustering


"""
Use sklearn.AgglomerativeClustering for clustering, Agglomerative is a better unsupervised clustering method than knn
"""

"""
Get all the champions and their match data
Return a dict contain the labels as key and corresponding champions as values
"""
def clusterChampions(cluster_num,conn):
    #print('enter')
    # 1. Get all champions with their match statistic and forms the features that're fed into the cluster
    champion = get_data(conn, 'Champion')
    matches=get_data(conn, 'Participants')
    #print(champion)
    all_champion_datas = []
    for c in champion:
        all_champion_datas.append(champion_data(c[0], matches))
    #print('get all champion',all_champion_datas)
    # from all_champion_data integrate a champion's all data into a single average one:
    all_features=[]
    fea_num=len(all_champion_datas[0]['JUNGLE'])
    #print('feature number',fea_num)
    #print(all_champion_datas)
    j=0
    for cham_data in all_champion_datas:
        current_cham_feature=np.zeros(fea_num)
        for cur_pos in cham_data:
            current_pos_data=cham_data[cur_pos]
            for i,fea in enumerate(current_pos_data):
                current_cham_feature[i]+=list(fea.values())[0]
        lanes=len(cham_data)
        #print('champion',j,champion[j][1],'lanes',lanes)
        current_cham_feature=list(current_cham_feature/lanes)
        all_features.append(current_cham_feature)
        j+=1
    # 2. Begin Agglomerative
    agg=AgglomerativeClustering(cluster_num,linkage='complete')
    agg.fit(all_features)
    # 3. fetch cluters with data
    clusters={}
    for i, label in enumerate(agg.labels_):
        if label not in clusters:
            clusters[int(label)]=[champion[i][0]]
        else:
            clusters[int(label)].append(champion[i][0])
    return clusters

"""
Input:
cluster: the trained total cluster
champion: the champion that we'd like to assign cluster
Return:
int: The cluster id of this champion
"""
def getChampionCluster(cluster,champion):
    for cid in cluster:
        if champion in cluster[cid]:
            return cid
    raise BaseException("Champion {} not found!".format(champion))

"""
Get champion list on one position ranked by winning rate and corresponding cluster type 
"""
def getChampionDataForLane(conn,pos,cluster):
    champions = get_data(conn, 'Champion')
    # 1. get this summoner's match histories, only need to know the times he use each champion, the cluster and lane of that champion
    participants = get_data(conn, 'Participants')
    champion_win=[]
    cham_cluster=[]
    for c in champions:
        cur_data=champion_data(c[0], participants)
        if pos not in cur_data:
            champion_win.append(0)
        else:
            target=cur_data[pos]
            #print(c[1],pos,'target ero',target)
            winrate=float(target[1]['win_rate'])
            choserate=float(target[0]['chosen_rate'])
            if choserate>=0.0005:
                champion_win.append(winrate)
            else:
                champion_win.append(0)
    cham_ids=np.argsort(np.array(champion_win))[::-1]
    #print('lol',pos,cham_ids)
    for id in cham_ids:
        cham_cluster.append(getChampionCluster(cluster,id))
    return cham_ids,cham_cluster



"""
Given a summoner, give him personalized recommended heros for different positions (each top n)
Return: a dict with position as key champios as values 
"""
def RecommendChampionsForUser(summoner,recommend_num,conn):

    champions=get_data(conn, 'Champion')
    # 1. get this summoner's match histories, only need to know the times he use each champion, the cluster and lane of that champion
    participants=get_data(conn, 'Participants')
    all_champion_datas = []
    for c in champions:
        all_champion_datas.append(champion_data(c[0], participants))

    clusters=clusterChampions(6,conn)
    summoner_matches={} # key is lane, values are {champion: used_time}
    # get count of all heros in each lane first
    for p in participants:
        if p[1]==summoner:
            cur_pos=get_position(p)
            if cur_pos!=None:
                champion=int(p[3])
                if cur_pos not in summoner_matches:
                    summoner_matches[cur_pos]=np.zeros(len(champions))
                    summoner_matches[cur_pos][champion]+=1
                else:
                    summoner_matches[cur_pos][champion]+=1
    #print('all raw data',summoner_matches)
    pos_top10_used={}
    # take the top 10 most commonly used heros for each lanes
    for pos in summoner_matches:
        chams=np.argsort(summoner_matches[pos])[::-1][:10]
        #print('original champion order',summoner_matches[pos])
        #print('top 10',chams)
        cluster=np.zeros(6)
        for cham_id in chams:
            if summoner_matches[pos][cham_id]!=0:
                cluster[getChampionCluster(clusters,cham_id)]+=1
        #print('original cluster num',cluster)
        cluster=np.argsort(cluster)[::-1]
        #print('ordered cluster',cluster)
        pos_top10_used[pos]=(chams,cluster)
    res={'JUNGLE':[],'TOP_LANE':[],'MID_LANE':[],'DUO_CARRY':[],'DUO_SUPPORT':[]}
    """
    recommend

    """
    for pos in res:
        pos_cham_by_winrate, pos_cham_cluster = getChampionDataForLane(conn, pos, clusters)
        if pos not in pos_top10_used:
            #print('get default recommendation',pos)
            for i,hero in enumerate(pos_cham_by_winrate):
                if i==recommend_num:
                    break
                res[pos].append(champions[hero][1])
        else:
            topheros,topcluster=pos_top10_used[pos]
            topused=set(topheros)
            #  1. Got all champions ordered by win rate in that lane
            count=0
            # in case one cluster num not enough
            for prefered_cluster in topcluster:
                found = False
                for idx, champ in enumerate(pos_cham_by_winrate):
                    if count==recommend_num:
                        found=True
                        break
                    # don't recommend commonly used heros
                    if champ in topused:
                        continue
                    if pos_cham_cluster[idx]==prefered_cluster:
                        res[pos].append(champions[champ][1])
                        count+=1
                if found:
                    break
    return res

# print recommend result
def printRecommendResult(res):
    result=[]
    for pos in res:
        heros=res[pos]
        num=len(heros)
        output="Top" + str(num) + "recommended champions in "+pos+":\t"+", ".join(heros)
        result.append(output)
    return '\n'.join(result)



if __name__=='__main__':
    conn = sqlite3.connect('lol.db')
    clusters=clusterChampions(6,conn)
    count=0
    for c in clusters:
        count+=len(clusters[c])
    print('cluster num',count)
    print(len(clusters))
    print(clusters)
    for c in clusters:
        print(c,type(c)==int)
        break
    print(printRecommendResult(RecommendChampionsForUser(35205845,5,conn)))