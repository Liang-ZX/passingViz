import utils as lib
import numpy as np
import os

ROOT = ".."
wholelist = {}
count = 0 
PLAYER = 30
MATCH_LEN = 38

wholetable = np.zeros((PLAYER, PLAYER))

def limit(P):
    pi = [1/11]*11
    pi = np.array(pi)
    print(pi.shape, P.shape)

    for i in range(PLAYER):
        pi = P @ pi
    return pi
        
def stationary(src):
    P = np.array(src[:11, :11])
    length = 11
    A = np.zeros((length, length))
    b = np.zeros((length, ))
    b[-1] = 1
    for i in range(length):
        P[i, :] = P[i, :] / (np.sum(P[i, :])+1e-6)
    tmp = P.T.copy()
    for i in range(length):
        tmp[i, i] -= 1
    A = tmp.copy()
    A[length-1, :] = 1

    if np.linalg.matrix_rank(A) == length:
        Pi = np.linalg.inv(A) @ b
        if np.abs(tmp[length-1, :] @ Pi) < 1e-4: 
            print(Pi)
        else:
            Pi = limit(P)
    else:
        Pi = limit(P)
    return Pi

if __name__ == "__main__":
    whole_stable = np.zeros((MATCH_LEN, 11))
    cur_stable = np.zeros((MATCH_LEN, 11))

    for match in range(MATCH_LEN):
        temp = np.zeros((PLAYER, ))
        player, adj = lib.get_passing_matrix(match+1, 'Huskies', 'ALL', 0, 100)
        length = 14
        P = adj.copy()
        for item in player:
            if item in wholelist:
                temp[player[item]] = int(wholelist[item])
            else:
                wholelist[item] = count
                temp[wholelist[item]] = int(player[item])
                count += 1
        for i in player:
            for j in player:
                wholetable[int(temp[player[i]]), int(temp[player[j]])] += adj[player[i], player[j]]
        print(match)

        player, adj = lib.get_passing_matrix(match+1, 'Huskies', '1H', 0, 45)
        cur_stable[match-1, :] = stationary(adj)

        length = 11
        P = np.zeros((length, length))
        for pl1 in player:
            for pl2 in player:
                if player[pl1] < 11 and player[pl2] < 11:
                    P[player[pl1], player[pl2]] = wholetable[wholelist[pl1], wholelist[pl2]]
        whole_stable[match, :] = stationary(P)

    vari = np.empty((MATCH_LEN, 2))

    for i in range(MATCH_LEN):
        vari[i, 0] = np.var((whole_stable[i, :]))
        vari[i, 1] = np.var((cur_stable[i, :]))
    np.savetxt(os.path.join(ROOT, 'result', 'vari_stable.csv'), vari, delimiter=',')
