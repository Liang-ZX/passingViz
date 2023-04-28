from get_micro_fea import get_eigenvector_of_match, get_clustering_of_match, get_closeness_of_match, \
    get_betweenness_of_match, get_algebraic_connectivity_of_match
import numpy as np
import csv
import os
import argparse
from tqdm import tqdm


ROOT = ".."

def write_betweenness():
    write_dir_1 = os.path.join(ROOT, "result/betweenness_mean.csv")
    write_dir_2 = os.path.join(ROOT, "result/betweenness_var.csv")
    csvFile1=open(write_dir_1,'w',newline='')
    csvFile2=open(write_dir_2,'w',newline='')
    writer1=csv.writer(csvFile1)
    writer2=csv.writer(csvFile2)
    for i in tqdm(range(1,39)):
        Huskies = []
        Huskies_clustering = get_betweenness_of_match(i,'Huskies')
        for k,v in Huskies_clustering.items():
            Huskies.append(v)
        Opponent = []
        Opponent_clustering = get_betweenness_of_match(i,'Opponent')
        for k,v in Opponent_clustering.items():
            Opponent.append(v)
        # print((i,np.mean(Huskies),np.mean(Opponent)))
        writer1.writerow((i,np.mean(Huskies),np.mean(Opponent)))
        writer2.writerow((i,np.var(Huskies),np.var(Opponent))) 


def write_closeness():
    write_dir_1 = os.path.join(ROOT, "result/closeness_mean.csv")
    write_dir_2 = os.path.join(ROOT, "result/closeness_var.csv")
    csvFile1=open(write_dir_1,'w',newline='')
    csvFile2=open(write_dir_2,'w',newline='')
    writer1=csv.writer(csvFile1)
    writer2=csv.writer(csvFile2)
    for i in tqdm(range(1,39)):
        Huskies = []
        Huskies_clustering = get_closeness_of_match(i,'Huskies')
        for k,v in Huskies_clustering.items():
            Huskies.append(v)
        Opponent = []
        Opponent_clustering = get_closeness_of_match(i,'Opponent')
        for k,v in Opponent_clustering.items():
            Opponent.append(v)
        # print((i,np.mean(Huskies),np.mean(Opponent)))
        writer1.writerow((i,np.mean(Huskies),np.mean(Opponent)))
        writer2.writerow((i,np.var(Huskies),np.var(Opponent))) 


def write_clustering():
    write_dir_1 = os.path.join(ROOT, "result/clustering_mean.csv")
    write_dir_2 = os.path.join(ROOT, "result/clustering_var.csv")
    csvFile1 = open(write_dir_1,'w',newline='')
    csvFile2 = open(write_dir_2,'w',newline='')
    writer1=csv.writer(csvFile1)
    writer2=csv.writer(csvFile2)
    for i in tqdm(range(1,39)):
        Huskies = []
        Huskies_clustering = get_clustering_of_match(i,'Huskies')
        for k,v in Huskies_clustering.items():
            Huskies.append(v)
        Opponent = []
        Opponent_clustering = get_clustering_of_match(i,'Opponent')
        for k,v in Opponent_clustering.items():
            Opponent.append(v)
        # print((i,np.mean(Huskies),np.mean(Opponent)))
        writer1.writerow((i,np.mean(Huskies),np.mean(Opponent)))
        writer2.writerow((i,np.var(Huskies),np.var(Opponent)))


def write_eigenvector_mean():
    write_dir = os.path.join(ROOT, "result/eigenvector_mean.csv")
    csvFile=open(write_dir,'w',newline='')
    writer=csv.writer(csvFile)
    for i in tqdm(range(1,39)):
        Huskies = []
        Huskies_eigenvector = get_eigenvector_of_match(i,'Huskies')
        for k,v in Huskies_eigenvector.items():
            Huskies.append(v)
        Opponent = []
        Opponent_eigenvector = get_eigenvector_of_match(i,'Opponent')
        for k,v in Opponent_eigenvector.items():
            Opponent.append(v)
        # print((i,np.mean(Huskies),np.mean(Opponent)))
        writer.writerow((i,np.mean(Huskies),np.mean(Opponent)))  


def write_eigenvector_var():
    write_dir = os.path.join(ROOT, "result/eigenvector_var.csv")
    csvFile=open(write_dir,'w',newline='')
    writer=csv.writer(csvFile)
    for i in tqdm(range(1,39)):
        Huskies = []
        Huskies_eigenvector = get_eigenvector_of_match(i,'Huskies')
        for k,v in Huskies_eigenvector.items():
            Huskies.append(v)
        Opponent = []
        Opponent_eigenvector = get_eigenvector_of_match(i,'Opponent')
        for k,v in Opponent_eigenvector.items():
            Opponent.append(v)
        # print((i,np.var(Huskies),np.var(Opponent)))
        writer.writerow((i,np.var(Huskies),np.var(Opponent)))      


def write_algebraic_connectivity():
    write_dir = os.path.join(ROOT, "result/algebraic_connectivity.csv")
    csvFile=open(write_dir,'w',newline='')
    writer=csv.writer(csvFile)
    for i in tqdm(range(1,39)):
        a = get_algebraic_connectivity_of_match(i,'Huskies')
        b = get_algebraic_connectivity_of_match(i,'Opponent')
        # print((i,a,b))
        writer.writerow((i,a,b))


def write_closeness_personal():
    write_dir = os.path.join(ROOT, "result/closeness_personal.csv")
    csvFile=open(write_dir,'w',newline='')
    writer=csv.writer(csvFile)
    all_player = set()
    file_dir = os.path.join(ROOT, "data/passingevents.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader)
    for i, row in enumerate(reader):
        if row[1] == 'Huskies' :
            all_player.add(row[2])
            all_player.add(row[3])
    csvfile.close()
    player_closeness = {}
    for player in all_player:
        player_closeness[player] = [0] * 38
    for i in range(0,38):
        Huskies_closeness = get_closeness_of_match(i,'Huskies')
        for player,closeness in Huskies_closeness.items():
            player_closeness[player][i] = closeness
    for player, v in player_closeness.items():
        writer.writerow((player,)+tuple(v))


def write_clustering_personal():
    write_dir = os.path.join(ROOT, "result/clustering_personal.csv")
    csvFile=open(write_dir,'w',newline='')
    writer=csv.writer(csvFile)
    all_player = set()
    file_dir = os.path.join(ROOT, "data/passingevents.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader)
    for i, row in enumerate(reader):
        if row[1] == 'Huskies' :
            all_player.add(row[2])
            all_player.add(row[3])
    csvfile.close()
    player_closeness = {}
    for player in all_player:
        player_closeness[player] = [0] * 38
    for i in range(0,38):
        Huskies_closeness = get_clustering_of_match(i,'Huskies')
        for player,closeness in Huskies_closeness.items():
            player_closeness[player][i] = closeness
    for player, v in player_closeness.items():
        writer.writerow((player,)+tuple(v))


def write_top_n_closeness():
    write_dir = os.path.join(ROOT, "result/top_5_closeness.csv")
    csvFile=open(write_dir,'w',newline='')
    writer=csv.writer(csvFile)
    for i in tqdm(range(1,39)):
        Huskies_closeness = get_clustering_of_match(i,'Huskies')
        Huskies_closeness = list(Huskies_closeness.values())
        Huskies_closeness.sort(reverse=True)
        H_points = sum(Huskies_closeness[:5])
        
        Opponent_closeness = get_clustering_of_match(i,'Opponent')
        Opponent_closeness = list(Opponent_closeness.values())
        Opponent_closeness.sort(reverse=True)
        O_points = sum(Opponent_closeness[:5])
        # print((i,H_points,O_points))
        writer.writerow((i,H_points,O_points))


def write_low_n_closeness():
    write_dir = os.path.join(ROOT, "result/low_5_closeness.csv")
    csvFile=open(write_dir,'w',newline='')
    writer=csv.writer(csvFile)
    for i in tqdm(range(1,39)):
        Huskies_closeness = get_clustering_of_match(i,'Huskies')
        Huskies_closeness = list(Huskies_closeness.values())
        Huskies_closeness.sort()
        l = Huskies_closeness
        H_points = sum(l[:5])
        
        Opponent_closeness = get_clustering_of_match(i,'Opponent')
        Opponent_closeness = list(Opponent_closeness.values())
        Opponent_closeness.sort()
        l = Opponent_closeness
        O_points = sum(l[:5])
        # print(Opponent_closeness)
        # print((i,H_points,O_points))
        writer.writerow((i,H_points,O_points))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--indicator', default='betweenness', type=str, help='indicator type in [betweenness, '
       'closeness, top_5_closeness, low_5_closeness, personal_closeness, clustering, personal_clustering, eigen_mean, eigen_var, alg_connectivity]')
    args = parser.parse_args()

    print("Please wait...")
    if args.indicator == "betweenness":
        write_betweenness()
    elif args.indicator == "closeness":
        write_closeness()
    elif args.indicator == "top_5_closeness":
        write_top_n_closeness()   # top 5
    elif args.indicator == "low_5_closeness":
        write_low_n_closeness()    # low 5
    elif args.indicator == "personal_closeness":
        write_closeness_personal()
    elif args.indicator == "clustering":
        write_clustering()
    elif args.indicator == "personal_clustering":
        write_clustering_personal()
    elif args.indicator == "eigen_mean":
        write_eigenvector_mean()
    elif args.indicator == "eigen_var":
        write_eigenvector_var()
    elif args.indicator == "alg_connectivity":
        write_algebraic_connectivity()
    else:
        raise NotImplementedError
