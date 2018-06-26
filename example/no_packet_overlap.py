import os
import sys
from os.path import dirname
import matplotlib.pyplot as plt

sys.path.append("../src/")
from figure_plot import *

def main():
    fig1, ax1 = plt.subplots(figsize=(5, 5)) #fig1: RSSI to multiple constant
    fig2, ax2 = plt.subplots(figsize=(5, 5)) #fig2: packet loss to multiple constant

    cwd = os.getcwd()

    delay = ["9k"]
    MC = [0.1, 0.5, 0.8, 0.9, 1, 2, 5, 10, 100, 500, 600, 700, 800]
    # MC = [0.1, 0.5, 1, 5]
    MC_str = ['100u', '500u', '800u', '900u', '1m', '2m', '5m', '10m', '100m', '500m', '600m', '700m', '800m']

    num_rv = [[0] * len(MC)] * len(delay)
    rssi_mean = [[0] * len(MC)] * len(delay)
    rssi_confidence_interval = [[0] * len(MC)] * len(delay)
    packet_loss = [[1.0] * len(MC)] * len(delay)

    for i in range(0, len(delay)):
        for j in range(0, len(MC)):
            file_path = dirname(cwd) + "/data/pdu200_delay" + delay[i] + "_MC" + MC_str[j] * 2 + "_br6.pcapng"
            rv_id = "23:23:23:23:23:23"
            num_rv[i][j], rssi_mean[i][j], rssi_confidence_interval[i][j] = read_file(file_path, rv_id)
            packet_loss[i][j] = (1000 - num_rv[i][j]) / 1000

        # plot RSSI to multiple constant
        # ignore the part of num_rv[i]=0
        for x in range(0, len(MC)):
            if (num_rv[i][x]):
                non_zero_start = i
                break
        errorbar_plot(ax1, num_rv[i], MC, rssi_mean[i], rssi_confidence_interval[i])
        line_plot(ax2, MC, packet_loss[i])

        # save figures
        fig1.savefig(dirname(cwd) + "/figure/no_packet_overlap_br6_RSSI.eps", format='eps', dpi=1000)
        fig2.savefig(dirname(cwd) + "/figure/no_packet_overlap_br6_Packetloss.eps", format='eps', dpi=1000)

    return 0

if __name__=="__main__":
    main()
    plt.show()