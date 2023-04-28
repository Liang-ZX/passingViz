import csv
from utils import get_passing_matrix, get_graph_from_matrix
import networkx as nx
import numpy as np
import os
import argparse


ROOT = ".."
# 用法：
# get_closeness_of_match(match_id,team):match_id为1,2,3之类，team为'Huskies'或'Opponent'
# get_betweenness_of_match(match_id,team):match_id为1,2,3之类，team为'Huskies'或'Opponent'

def get_player_in_match_time(match_id,team,player):
    file_dir = os.path.join(ROOT, "data/fullevents.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader) #跳过第一行
    
    time = 90
    for i, row in enumerate(reader):
        if row[6] != 'Substitution':
            continue
        if eval(row[0]) < match_id :
            continue
        if eval(row[0]) > match_id : 
            break
        if team == 'Huskies' and row[1] != 'Huskies' :
            continue
        if team == 'Opponent' and row[1] == 'Huskies' :
            continue
        if row[2] == player:
            if row[4] == '1H':
                time = time - 45 - eval(row[5])/60
            else:
                time = time - (45 - eval(row[5])/60)
        if row[3] == player:
            if row[4] == '1H':
                time = time - (45 - eval(row[5])/60)
            else:
                time = time - (45 + eval(row[5])/60)
    return time

def get_old_closeness_of_match(match_id,team):
    player_index,A = get_passing_matrix(match_id,team,'ALL')
    G = get_graph_from_matrix(A)
    closeness = nx.algorithms.centrality.closeness_centrality(G)
    player_closeness = {}
    for player,index in player_index.items():
        player_closeness[player] = closeness[index]
    return player_closeness


def get_closeness_of_match(match_id,team, timespan=10):
    player_count = {}
    player_closeness = {}
    # 上下半场分开,timespan分钟算一次
    for i in range(1,3):
        for j in range(50//timespan):
            if i == 1:
                player_index,A = get_passing_matrix(match_id,team,'1H',j*timespan,(j+1)*timespan)
            else:
                player_index,A = get_passing_matrix(match_id,team,'2H',j*timespan,(j+1)*timespan)
            G = get_graph_from_matrix(A)
            closeness = nx.algorithms.centrality.closeness_centrality(G)
            for player,index in player_index.items():
                if player_count.get(player) is None:
                    player_count[player] = 1
                else:
                    player_count[player] = player_count[player] + 1
                if player_closeness.get(player) is None:
                    player_closeness[player] = closeness[index]
                else:
                    player_closeness[player] = player_closeness[player] + closeness[index]
    for name in player_closeness:
        player_closeness[name] = player_closeness[name]/player_count[name]
    return player_closeness


def write_match_closeness(match_id,team, timespan=10):
    all_player_index,matrix = get_passing_matrix(match_id,team,'ALL')
    player_closeness = {}
    for player in all_player_index:
        player_closeness[player] = [0]*timespan
    for i in range(1,3):
        for j in range(0,5):
            if i == 1:
                player_index,A = get_passing_matrix(match_id,team,'1H',j*timespan,(j+1)*timespan)
            else:
                player_index,A = get_passing_matrix(match_id,team,'2H',j*timespan,(j+1)*timespan)
            G = get_graph_from_matrix(A)
            closeness = nx.algorithms.centrality.closeness_centrality(G)
            for player,index in player_index.items():
                player_closeness[player][(i-1)*5+j] = closeness[index]
    write_dir = os.path.join(ROOT, "result/match_%d_closeness_%s.csv" % (match_id, team))
    csvFile=open(write_dir,'w',newline='')
    writer=csv.writer(csvFile)
    for player in player_closeness:
        writer.writerow((player,)+tuple(player_closeness[player]))


def get_betweenness_of_match(match_id,team, timespan=10):
    player_count = {}
    player_betweenness = {}
    # 上下半场分开,timespan分钟算一次
    for i in range(1,3):
        for j in range(50//timespan):
            if i == 1:
                player_index,A = get_passing_matrix(match_id,team,'1H',j*timespan,(j+1)*timespan)
            else:
                player_index,A = get_passing_matrix(match_id,team,'2H',j*timespan,(j+1)*timespan)
            G = get_graph_from_matrix(A)
            betweenness = nx.betweenness_centrality(G)
            for player,index in player_index.items():
                if player_count.get(player) is None:
                    player_count[player] = 1
                else:
                    player_count[player] = player_count[player] + 1
                if player_betweenness.get(player) is None:
                    player_betweenness[player] = betweenness[index]
                else:
                    player_betweenness[player] = player_betweenness[player] + betweenness[index]
    for name in player_betweenness:
        player_betweenness[name] = player_betweenness[name]/player_count[name]
    return player_betweenness


def get_clustering_of_match(match_id,team, timespan=10):
    player_count = {}
    player_clustering = {}
    # 上下半场分开,timespan分钟算一次
    for i in range(1,3):
        for j in range(50//timespan):
            if i == 1:
                player_index,A = get_passing_matrix(match_id,team,'1H', j*timespan,(j+1)*timespan)
            else:
                player_index,A = get_passing_matrix(match_id,team,'2H', j*timespan,(j+1)*timespan)
            G = get_graph_from_matrix(A)
            clustering = nx.algorithms.cluster.clustering(G)

            for player,index in player_index.items():
                if player_count.get(player) is None:
                    player_count[player] = 1
                else:
                    player_count[player] = player_count[player] + 1
                if player_clustering.get(player) is None:
                    player_clustering[player] = clustering[index]
                else:
                    player_clustering[player] = player_clustering[player] + clustering[index]
    for name in player_clustering:
        player_clustering[name] = player_clustering[name]/player_count[name]
    return player_clustering


def get_eigenvector_of_match(match_id,team, timespan=15):
    player_count = {}
    player_eigenvector = {}
    # 上下半场分开,timespan分钟算一次
    for i in range(1,3):
        for j in range(50//timespan):
            if i == 1:
                player_index,A = get_passing_matrix(match_id,team,'1H',j*timespan,(j+1)*timespan)
            else:
                player_index,A = get_passing_matrix(match_id,team,'2H',j*timespan,(j+1)*timespan)
            G = get_graph_from_matrix(A)
            eigenvector = nx.algorithms.centrality.eigenvector_centrality_numpy(G)
            for player,index in player_index.items():
                if player_count.get(player) is None:
                    player_count[player] = 1
                else:
                    player_count[player] = player_count[player] + 1
                if player_eigenvector.get(player) is None:
                    player_eigenvector[player] = eigenvector[index]
                else:
                    player_eigenvector[player] = player_eigenvector[player] + eigenvector[index]
    for name in player_eigenvector:
        player_eigenvector[name] = player_eigenvector[name]/player_count[name]
    return player_eigenvector


def get_algebraic_connectivity_of_match(match_id,team):
    alg_conn = 0
    player_index,A = get_passing_matrix(match_id,team,'ALL')
    S = []
    for i in range(0,A.shape[0]):
        S.append(0)
        for j in range(0,A.shape[0]):
            if i != j:
                S[i] = S[i] + A[i][j] + A[j][i]
    for i in range(0,A.shape[0]):
        for j in range(i+1,A.shape[0]):
            A[i][j] = (A[i][j]+A[j][i]) / 2
            A[j][i] = A[i][j]
    A = -A
    for i in range(0,A.shape[0]):
        A[i][i] = S[i]
    eigenvalue,featurevector = np.linalg.eig(A)
    eigenvalue.sort()
    return 1/eigenvalue[1]


def get_match_info(match_id,team, timespan):
    closeness = get_closeness_of_match(match_id, team, timespan)
    print("Calculate Clossness Finish")
    betweenness = get_betweenness_of_match(match_id, team, timespan)
    print("Calculate Betweeness Finish")
    clustering = get_clustering_of_match(match_id, team, timespan)
    print("Calculate Clustering Finish")
    eigenvector = get_eigenvector_of_match(match_id, team, timespan=max(timespan, 15))
    print("Calculate Eigenvector Finish")
    print("Write ...")
    write_dir = os.path.join(ROOT, "result/match_%d_%s_info.csv" % (match_id, team))
    csvFile=open(write_dir,'w',newline='')
    writer=csv.writer(csvFile)
    writer.writerow(('player','closeness','betweenness','clustering','eigenvector'))
    for k in closeness:
        writer.writerow((k,closeness[k],betweenness[k],clustering[k],eigenvector[k]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--match_id', default=1, type=int, help='Match ID')
    parser.add_argument('--team', default='Huskies', type=str, help='Team Name in [Huskies, Opponent]')
    parser.add_argument('--time_span', default=10, type=int, help='Time Span')
    args = parser.parse_args()

    get_match_info(args.match_id, args.team, args.time_span)
    # print(get_player_in_match_time(38,'Opponent','Opponent14_M6'))

    # 'Huskies'或'Opponent'
    # write_match_closeness(1,'Huskies')
