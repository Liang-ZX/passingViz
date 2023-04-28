import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os


ROOT=".."

def read_data(flag = False):
    file_dir = os.path.join(ROOT, "data/passingevents.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader)

    members = []; tmp_member = set(); players = set()
    passes = []; tmp_pass = {}
    tmpid = 0

    for i, row in enumerate(reader):
        if row[1] != 'Huskies':
            continue
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
            if (row[2], row[3]) in tmp_pass:
                tmp_pass[(row[2], row[3])] = tmp_pass[(row[2], row[3])] + 1
            else:
                tmp_pass[(row[2], row[3])] = 1
    members.append(list(tmp_member))
    passes.append(dict(tmp_pass))
    csvfile.close() 
    players = list(players)
    players.sort()
    player_index = {}
    for i in range(len(players)):
        player_index[players[i]] = i
    if flag == True:
        print("player_index_map:", player_index)
        return members, passes, player_index, players
    # print(passes[1][('Huskies_M3', 'Huskies_D3')])
    else:
        return members, passes, player_index
    
def build_matrix():
    members, passes, player_index, players = read_data(flag = True)
    adj_matrix = np.zeros((38,len(players),len(players)))
    for i in range(38):
        for player1, player2 in passes[i+1]:
            adj_matrix[i][player_index[player1]][player_index[player2]] = passes[i+1][(player1, player2)]
        b = adj_matrix[i]
        aa = []
        for k in range(len(players)-1, -1, -1):
            if players[k] not in members[i+1]:
                b = np.delete(b, k, axis = 1)
            else:
                aa.append(k)
        if not os.path.exists(os.path.join(ROOT, "data/adj")):
            os.makedirs(os.path.join(ROOT, "data/adj"))
        write_dir = os.path.join(ROOT, "data/adj/adj_matrix"+str(i+1)+".csv")
        csvFile=open(write_dir,'w',newline='')
        writer=csv.writer(csvFile)
        aa.reverse()
        writer.writerow((None,)+tuple(aa))
        for j in range(len(players)):
            if players[j] in members[i+1]:
                writer.writerow((j,)+tuple(b[j]))
        csvFile.close()


if __name__ == "__main__":
    build_matrix()