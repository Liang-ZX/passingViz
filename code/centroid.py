import csv
import argparse
import numpy as np
import math
import os
from tqdm import tqdm
from utils import read_match


ROOT=".."

def read_data_with_pos():
    file_dir = os.path.join(ROOT, "data/passingevents.csv")
    csvfile = open(file_dir)
    reader = csv.reader(csvfile)
    next(reader)
    passes = {}
    for row in reader:
        time = eval(row[5])
        if row[4] == '2H':
            time += 3000
        if (eval(row[0]), row[1]) in passes:
            passes[eval(row[0]), row[1]].append(list([row[2], row[3], time, eval(row[7]),
                                                      eval(row[8]),eval(row[9]),eval(row[10])]))
        else:
            passes[eval(row[0]), row[1]] = [[row[2], row[3], time, eval(row[7]),
                                             eval(row[8]),eval(row[9]),eval(row[10])],]
    return passes


def centroid(matchID = 1, host=True, timespan = 5):
    passes = read_data_with_pos()
    xplayer = {}; yplayer = {}; j = 0
    xplayer_pos = {}; yplayer_pos = {}; xtmp = []; ytmp = []
    xplayers_all = []; yplayers_all = []

    match_map, opponent_map = read_match()
    if host:
        teamID = 'Huskies'
    else:
        teamID = opponent_map[matchID]
    for data in passes[(matchID, teamID)]:
        time = data[2]        
        if time > (j+1) * 60 * timespan:            
            for key in xplayer:                
                xtmp.append(np.mean(xplayer[key]))
                ytmp.append(np.mean(yplayer[key]))
                if key in xplayer_pos:
                    xplayer_pos[key] = np.append(xplayer_pos[key], np.mean(xplayer[key]))
                    yplayer_pos[key] = np.append(yplayer_pos[key], np.mean(yplayer[key]))
                else:
                    xplayer_pos[key] = np.array([np.mean(xplayer[key]),])
                    yplayer_pos[key] = np.array([np.mean(yplayer[key]),])
            xplayer.clear(); yplayer.clear()
            xplayers_all.append(list(xtmp))
            yplayers_all.append(list(ytmp))
            xtmp.clear(); ytmp.clear()
            j = j+1
            if j >= math.ceil(100.0/timespan):
                break            
        if data[0] in xplayer:
            xplayer[data[0]] = np.append(xplayer[data[0]], data[3])
            yplayer[data[0]] = np.append(xplayer[data[0]], data[4])
        else:
            xplayer[data[0]] = np.array([data[3],])
            yplayer[data[0]] = np.array([data[4],])
        if data[1] in xplayer:
            xplayer[data[1]] = np.append(xplayer[data[0]], data[5])
            yplayer[data[1]] = np.append(xplayer[data[0]], data[6])
        else:
            xplayer[data[1]] = np.array([data[5],])
            yplayer[data[1]] = np.array([data[6],])        
    
    xans_mean = []; xans_standard = []
    yans_mean = []; yans_standard = []    
    for item in xplayers_all:
        item = np.array(item)
        xans_mean.append(np.mean(item))
        xans_standard.append(np.std(item))
    for item in yplayers_all:
        item = np.array(item)
        yans_mean.append(np.mean(item))
        yans_standard.append(np.std(item))
    std_dist = []
    for i in range(len(xplayers_all)):
        D = np.sqrt((np.array(xplayers_all[i])-xans_mean[i])**2 + (np.array(yplayers_all[i])-yans_mean[i])**2)
        std_dist.append(np.std(np.array(D)))
    return xans_mean, xans_standard, yans_mean, yans_standard, std_dist


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--time_span', default=5, type=int, help='Time Span')
    args = parser.parse_args()

    match_map, opponent_map = read_match()
    write_dir = os.path.join(ROOT, "result/centroid.csv")
    csvFile = open(write_dir, 'w', newline='')
    writer = csv.writer(csvFile)
    writer.writerow(('matchID', 'Huskies_xmean', 'Huskies_ymean', 'Huskies_std',
                     'opponentID', 'opponent_xmean', 'opponent_ymean', 'opponent_std'))

    for i in tqdm(range(38)):
        xmean, xstd, ymean, ystd, std_dist = centroid(matchID=i + 1, timespan=args.time_span)
        xmean2, xstd2, ymean2, ystd2, std_dist2 = centroid(matchID=i + 1, host=False, timespan=args.time_span)
        writer.writerow((i + 1, list(xmean), list(ymean), list(std_dist), opponent_map[i + 1], list(xmean2),
                         list(ymean2), list(std_dist2)))
    csvFile.close()

        