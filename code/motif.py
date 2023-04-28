import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse


ROOT = ".."
def read_data_with_time():
    file_dir = os.path.join(ROOT, "data/passingevents.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader)

    members = []; tmp_member = set(); players = set()
    passes = []; tmp_pass = []
    tmpid = 0

    for i, row in enumerate(reader):
        if row[1] != 'Huskies':
            continue
        if row[6] in ['Head pass', 'Simple pass', 'Launch', 'High pass', 'Hand pass', 'Smart pass', 'Cross']:
            if tmpid != eval(row[0]):
                members.append(list(tmp_member))
                passes.append(list(tmp_pass))
                tmp_member.clear()
                tmp_pass.clear()
                tmpid = tmpid + 1
            tmp_member.add(row[2])
            tmp_member.add(row[3])
            players.add(row[2]); players.add(row[3])
            time = eval(row[5])
            if row[4] == '2H':
                time += 3000
            tmp_pass.append([row[2], row[3], time])
    members.append(list(tmp_member))
    passes.append(list(tmp_pass))
    csvfile.close()
    
    players = list(players)
    players.sort()
    player_index = {}
    for i in range(len(players)):
        player_index[players[i]] = i
    
#     print(passes[1])
    return members, passes, players, player_index


def motif(matchID, opponentID = None):
    if opponentID == None:
        members, passes, players, player_index = read_data_with_time()
        W = motif_single(members[matchID], passes[matchID])
    else:
        members, passes = read_other_team()
        W = motif_single(members[matchID], passes[matchID])
    return W
        
    
def motif_single(members, passes, mydict = None):
    length = 0; array = {}
    W = np.zeros(5)
    for i in range(len(passes)-2, 0, -1):
        if passes[i][1] == passes[i+1][0] and passes[i+1][2] - passes[i][2] < 20:
            length = length + 1
            continue
        if passes[i-1][1] == passes[i][0] and passes[i][2] - passes[i-1][2] < 20:
            continue
        del(passes[i])
        if length >= 3:
            for j in range(length-2):
                A = passes[i+j][0]; B = passes[i+j][1]; C = passes[i+j+1][1]; D = passes[i+j+2][1]
                if (A,B,C,D) in array:
                    array[(A,B,C,D)] += 1
                else:
                    array[(A,B,C,D)] = 1
                if A == C:
                    if B == D:
                        W[0] += 1  # ABAB
                    else:
                        W[1] += 1  # ABAC
                else:
                    if A == D:
                        W[2] += 1  # ABCA
                    else:
                        if B == D:  
                            W[3] += 1  #ABCB
                        else:
                            W[4] += 1  #ABCD
        length = 0
    
    if mydict != None:
        for key in array:
            if array[key] >= 2:
                if key in mydict:
                    mydict[key] += array[key]
                else:
                    mydict[key] = array[key]
        return mydict
    else:
        return W


def read_other_team():
    file_dir = os.path.join(ROOT, "data/passingevents.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader)

    members = []; tmp_member = set(); players = set()
    passes = []; tmp_pass = []
    tmpid = 0

    for i, row in enumerate(reader):
        if row[1] == 'Huskies':
            continue
        if row[6] in ['Head pass', 'Simple pass', 'Launch', 'High pass', 'Hand pass', 'Smart pass', 'Cross']:
            if tmpid != eval(row[0]):
                members.append(list(tmp_member))
                passes.append(list(tmp_pass))
                tmp_member.clear()
                tmp_pass.clear()
                tmpid = tmpid + 1
            tmp_member.add(row[2])
            tmp_member.add(row[3])
            
            tmp_pass.append([row[2], row[3], eval(row[5]), row[1]])
    members.append(list(tmp_member))
    passes.append(list(tmp_pass))
    csvfile.close()
    
#     print(passes[1])
    return members, passes


def unnamed_motif():
    write_dir = os.path.join(ROOT, "result/motif_3pass.csv")
    csvFile = open(write_dir, 'w', newline='')
    writer = csv.writer(csvFile)
    writer.writerow(('matchID', 'Huskies_ABAB', 'Huskies_ABAC', 'Huskies_ABCA',
                     'Huskies_ABCB', 'Huskies_ABCD', 'opponent_ABAB', 'opponent_ABAC', 'opponent_ABCA', 'opponent_ABCB',
                     'opponent_ABCD'))

    print("================================================================================")
    print("The 5 number are the count of (ABAB, ABAC, ABCA, ABCA, ABCB, ABCD) respectively.")
    print("================================================================================")
    print('MatchID\t', "Huskies\t\t Opponent")
    for i in range(38):
        W1 = motif(i+1).astype(np.int64)
        W2 = motif(i+1, 'opponent').astype(np.int64)
        print(i+1, "\t", W1,"\t", W2)
        writer.writerow((i+1,)+tuple(W1)+tuple(W2))
        # W = W1 - W2
        # print('MatchID: '+str(i+1), W)
    csvFile.close()

def named_motif():
    mydict = {}
    members, passes, players, player_index = read_data_with_time()
#     members, passes = read_other_team()
    for i in range(38):
        motif_single(members[i+1], passes[i+1], mydict=mydict)
    for key in mydict:
        if mydict[key] >= 4:
            print(key, mydict[key])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='unnamed', type=str,
                        help='[unnamed/named] => [flow motif/passing network motif]')
    args = parser.parse_args()
    
    if args.type == "unnamed":
        unnamed_motif()
    elif args.type == "named":
        named_motif()
    else:
        raise NotImplementedError
