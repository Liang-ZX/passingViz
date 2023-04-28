import csv
import networkx as nx
import numpy as np
import os

ROOT = ".."
# match_id为比赛序号1-38;team可选为Huskies或Opponent;
# half为半场，可选1H,2H,ALL;
# time_beg,time_end为时间的开始与结束，以分钟为单位
def get_passing_matrix(match_id, team, half, time_beg=0, time_end=0):
    # row[0] 为 match_id;row[1] 为teamID
    # row[2],[3]为source player和destination player
    # row[4] 为MatchPeriod;row[5] 为动作的时间
    file_dir = os.path.join(ROOT, "data/passingevents.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader)  # 跳过第一行

    players_index = {}

    p_index = 0  # player的index
    adj_matrix = np.zeros((20, 20))
    for i, row in enumerate(reader):
        if eval(row[0]) != match_id:
            continue
        if team == 'Huskies' and row[1] != 'Huskies':
            continue
        if team == 'Opponent' and row[1] == 'Huskies':
            continue
        if half != 'ALL' and half != row[4]:
            continue
        if half == 'ALL' or time_beg * 60 < eval(row[5]) < time_end * 60:
            if players_index.get(row[2]) is None:
                players_index[row[2]] = p_index
                p_index = p_index + 1
            if players_index.get(row[3]) is None:
                players_index[row[3]] = p_index
                p_index = p_index + 1
            s_index = players_index[row[2]]
            d_index = players_index[row[3]]
            adj_matrix[s_index][d_index] = adj_matrix[s_index][d_index] + 1
    csvfile.close()
    adj_matrix = adj_matrix[:len(players_index), :len(players_index)]
    return players_index, adj_matrix


def get_graph_from_matrix(adj_matrix):
    g = nx.DiGraph()
    node_num = adj_matrix.shape[0]
    for i in range(node_num):
        g.add_node(i)
    for i in range(node_num):
        for j in range(node_num):
            if i != j and adj_matrix[i][j] > 0:
                g.add_edge(i, j, weight=adj_matrix[i][j])
    return g


def read_match():
    file_dir = os.path.join(ROOT, "data/matches.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader)

    match_map = {}
    opponent_map = [-1,]
    for row in reader:
        opponentID = row[1]
        opponent_map.append(opponentID)
        if opponentID in match_map:
            match_map[opponentID].append(list([eval(row[0]), row[2], eval(row[3]), eval(row[4]), row[5]]))
        else:
            match_map[opponentID] = [[row[0], row[2], row[3], row[4], row[5]],]
    return match_map, opponent_map
