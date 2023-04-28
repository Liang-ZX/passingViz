import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy import interpolate
import os
import argparse


MATCH_LEN = 38
MAX_TOUCH = 500
DISCRETE_POINT_NUM = 300

ROOT=".."

def importpass(host=True):
    '''
    @ Function:
        Import passing data and extract time-spiral original data

    '''
    file_dir = os.path.join(ROOT, "data/passingevents.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader)

    members = []
    tmp_member, players = set(), set()
    passes, tmp_pass = [], {}
    tmpid = 0
    pos = {}
    touch = {}
    half_index = {}
    half_index['1H'] = 0
    half_index['2H'] = 1

    prev = '-1'
    for i, row in enumerate(reader):
        if (host and row[1] != 'Huskies') or (not host and row[1] == 'Huskies'):
            continue
        if row[0] != prev: #每场比赛开始前清零
            touch = {}
        prev = row[0] # 比赛之间触球次数清零

        if row[6] in ['Head pass', 'Simple pass', 'Launch', 'High pass', 'Hand pass', 'Smart pass', 'Cross']:
            if tmpid != eval(row[0]):
                members.append(list(tmp_member))
                passes.append(dict(tmp_pass))
                tmp_member.clear()
                tmp_pass.clear()
                tmpid = tmpid + 1
            tmp_member.add(row[2])
            tmp_member.add(row[3])
            players.add(row[2]); players.add(row[3])
            if row[2] in touch:
                touch[row[2]] += 1
            else:
                touch[row[2]] = 1
            if row[3] in touch:
                touch[row[3]] += 1
            else:
                touch[row[3]] = 1
            
            if (row[2], row[3]) in tmp_pass:
                tmp_pass[(row[2], row[3])] += 1
            else:
                tmp_pass[(row[2], row[3])] = 1
            if row[5] == 0:
                print('!!!', row[7], row[8])
            #Transform to meters
            pos[(row[0], row[2], str(row[4]), str(row[5]), touch[row[2]])] = (float(row[7])*1.1, float(row[8])*0.75)
            pos[(row[0], row[3], str(row[4]), str(row[5]), touch[row[3]])] = (float(row[9])*1.1, float(row[10])*0.75) 
            

    members.append(list(tmp_member))
    passes.append(dict(tmp_pass))
    csvfile.close()


    players = list(players); player_index = {}
    for i in range(len(players)):
        player_index[players[i]] = i
    # print(members)
    # print(passes[1][('Huskies_M3', 'Huskies_D3')])

    time_rec = {}
    distance = {}

    pos_center = np.zeros((MATCH_LEN, len(players), 2))
    pos_disper = np.zeros((MATCH_LEN, len(players), 2))

    
    temp_pos = np.zeros((len(players), MAX_TOUCH, 2))
    on_court = np.zeros((len(players), MATCH_LEN))
    real_touch = np.zeros((len(players), MATCH_LEN))
    
    prev = '1'
    for info in pos:
        gameID, player, half, times, touches = info
        if int(touches) == 0: # 判断是否上过场
            continue

        on_court[player_index[player], int(gameID)-1] = 1 #记录备用
        real_touch[player_index[player], int(gameID)-1] = int(touches) #记录触球数据

        if gameID != prev: #计算上一场比赛数据
            for j in range(len(players)):
                touch_tmp = int(real_touch[j, int(prev)-1]) 
                if touch_tmp != 0:
                    pos_center[int(prev)-1, j, 0] = np.mean(temp_pos[j, :touch_tmp, 0])
                    pos_center[int(prev)-1, j, 1] = np.mean(temp_pos[j, :touch_tmp, 1])
                    pos_disper[int(prev)-1, j, 0] = np.var(temp_pos[j, :touch_tmp, 0])
                    pos_disper[int(prev)-1, j, 1] = np.var(temp_pos[j, :touch_tmp, 1])
            temp_pos = np.zeros((len(players), MAX_TOUCH, 2)) # 清零
        
        prev = gameID
        
        tmp1, tmp2 = pos[(gameID, player, half, times, touches)]
        # print(tmp1, tmp2)
        # print(times)
        
        temp_pos[player_index[player], int(touches)-1, 0] = float(tmp1)        
        temp_pos[player_index[player], int(touches)-1, 1] = float(tmp2)

        if (gameID, player) not in distance:
            distance[(gameID, player)] = 0
        else:
            if player in time_rec:
                if float(times) - time_rec[player] < 100:
                    gap = pow(temp_pos[player_index[player], int(touches)-1, 0]-temp_pos[player_index[player], int(touches)-2, 0], 2)+pow(temp_pos[player_index[player], int(touches)-1, 1]-temp_pos[player_index[player], int(touches)-2, 1], 2)
                    if gap < 100: # 跑动距离比较近（10个单位以内）
                        distance[(gameID, player)] += gap
            time_rec[player] = float(times)
    # print('distance: ', distance)
    # print('center: ', pos_center)
    # print('touch: ', touches)
    for j in range(len(players)):
        pos_center[int(prev)-1, j, 0] = np.mean(temp_pos[j, :int(touches), 0])
        pos_center[int(prev)-1, j, 1] = np.mean(temp_pos[j, :int(touches), 1])
        pos_disper[int(prev)-1, j, 0] = np.var(temp_pos[j,  :int(touches), 0])
        pos_disper[int(prev)-1, j, 1] = np.var(temp_pos[j,  :int(touches), 1])

    return members, pos_center, player_index, pos_disper, distance, passes


def passing_net(matchrange, host, members, pos_center, player_index, pos_disper, distance, passes):
    '''
    @ Function:
        Visualization of passing net
    '''
    for matches in matchrange:
        
        # 转成制图格式
        center = {}
        labels = {}
        disper = []
        print("---------------------------------------------------------")
        print("Match id", matches+1)
        print("---------------------------------------------------------")
        print("Players on court:", members[matches+1])
        
        for j in members[matches+1]:
            center[j] = pos_center[matches, player_index[j], :]
            mobility = np.sqrt(pow(pos_disper[matches, player_index[j], 0], 2)+pow(pos_disper[matches, player_index[j], 1], 2))*2+distance[str(matches+1), j]*3
            disper.append(mobility)
        print('Center: ', center)
        print('Mobility: ', disper)
        G = nx.DiGraph() #directed graph

        for player in members[matches+1]:
            G.add_node(player)   # add node 
            if player[-3] == '_':
                labels[player] = player[-2:]
            else:
                labels[player] = player[-3:]

        for player1, player2 in passes[matches+1]:
            G.add_edge(player1, player2, weight = passes[matches+1][(player1, player2)]) # 配置边的权重
        plt.figure(figsize=(10, 9))
        M = G.number_of_edges()

        edge_colors = range(1, M + 1)
        node_sizes = [3 + 10 * i for i in range(len(G))]
        edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

        pos = center
        edges = nx.draw_networkx_edges(
            G,
            pos,
            node_size=node_sizes,
            arrowstyle="->",
            arrowsize=10,
            edge_color=edge_colors,
            edge_cmap=plt.cm.inferno,
            width=6,
        )
        for i in range(M):
            edges[i].set_alpha(edge_alphas[i])

        pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.inferno)
        pc.set_array(edge_colors)
        plt.colorbar(pc)
        ax = plt.gca()
        ax.set_axis_off()

        nx.draw_networkx_labels(G,pos,labels, font_size=12, font_color='black')
        n_color = '#66FF99' if host else '#FFCC99'
        nx.draw(G, pos, node_color=n_color, node_size=disper, with_labels=False) #

        # # draw map
        # lx1 = [0, 100, 100, 0, 0]
        # ly1 = [0, 0, 90, 90, 0]
        # ax.plot(lx1, ly1, lw=2, zorder=-1)
        # plt.show()
        if not os.path.exists(os.path.join(ROOT, 'result/fig/')):
            os.makedirs(os.path.join(ROOT, 'result/fig/'))
        team = 'host' if host else 'guest'
        plt.savefig(os.path.join(ROOT, 'result/fig/network_'+str(matches+1)+ '_' + team + '.jpg'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--match_id', default=1, type=int, help='Match ID')
    parser.add_argument('--guest', action='store_true', help='Whether to draw the graph of the guest team?')
    args = parser.parse_args()
    
    matchid = [args.match_id - 1]
    host = not args.guest
    members, pos_center, player_index, pos_disper, distance, passes = importpass(host=host)
    passing_net(matchid, host, members, pos_center, player_index, pos_disper, distance, passes)