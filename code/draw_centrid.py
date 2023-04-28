import matplotlib.pyplot as plt
from centroid import centroid
import argparse
import os

ROOT = ".."
def draw_pitcure(matchID, timespan):
    xmean, xstd, ymean, ystd, std_dist = centroid(matchID=matchID, timespan=timespan)
    xmean2, xstd2, ymean2, ystd2, std_dist2 = centroid(matchID=matchID, host=False, timespan=timespan)
    plt.figure(figsize=(9.6, 4.8))
    plt.plot(xmean, marker="*", label="Huskies")
    plt.plot(xmean2, marker="*", color='r', label="Opponent")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Position along the direction of the vertical goal line")
    # plt.show()
    plt.savefig(os.path.join(ROOT, 'result/fig/centroid_' + str(matchID) + '.jpg'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--match_id', default=1, type=int, help='Match ID')
    parser.add_argument('--time_span', default=5, type=int, help='Time Span')
    args = parser.parse_args()

    draw_pitcure(args.match_id, args.time_span)
