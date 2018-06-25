import os
import pyshark
from math import *

import matplotlib
from matplotlib.legend_handler import HandlerErrorbar

import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

def read_file(filepath, rvid):
    num_rec = 0
    rssi = []
    cap = pyshark.FileCapture(filepath)
    for pkt in cap:
        try:
            if (pkt.wlan.sa == rvid):
                num_rec += 1
                rssi.append(int(pkt.wlan_radio.signal_dbm))
        except:
            continue

    if (num_rec):
        rssi_mean = sum(rssi) / len(rssi)
        z_critical = stats.norm.ppf(q=0.975)  # Get the z-critical value*
        rssi_std = np.std(rssi)
        margin_of_error = z_critical * (rssi_std / np.sqrt(len(rssi)))
        rssi_confidence_interval = (rssi_mean - margin_of_error, rssi_mean + margin_of_error)
    else:
        rssi_mean = 0
        rssi_confidence_interval = (0, 0)
    print(num_rec, rssi_mean, rssi_confidence_interval)
    return num_rec, rssi_mean, rssi_confidence_interval


def main():
    fig1, ax1 = plt.subplots(figsize=(5, 4)) #fig1: RSSI to multiple constant
    fig2, ax2 = plt.subplots(figsize=(5, 4)) #fig2: packet loss to multiple constant

    cwd = os.getcwd()

    delay = ["9k"]
    MC = [0.1, 0.5, 1, 5, 10, 100, 500, 600, 700, 800]
    x_axis = [log10(x) for x in MC]
    MC_str = ['100u', '500u', '1m', '5m', '10m', '100m', '500m', '600m', '700m', '800m']

    num_rv = [[0] * len(MC)] * len(delay)
    rssi_mean = [[0] * len(MC)] * len(delay)
    rssi_confidence_interval = [[0] * len(MC)] * len(delay)

    for i in range(0, len(delay)):
        for j in range(0, len(MC)):
            file_path = cwd + "/Data/pdu200_delay" + delay[i] + "_MC" + MC_str[j] * 2 + "_br6.pcapng"
            rv_id = "23:23:23:23:23:23"
            num_rv[i][j], rssi_mean[i][j], rssi_confidence_interval[i][j] = read_file(file_path, rv_id)


        ax1.errorbar(x=x_axis,
                     y=rssi_mean[i],
                     yerr=[(top - bot) / 2 for top, bot in rssi_confidence_interval[i]],
                     fmt='o')
                    # label='$MC1=0.5$')

        ax2.plot(x_axis, num_rv[i],
                 c=(0.25, 0.25, 1.00),
                 lw=2,
                 zorder=10)

        # font = {'family': 'serif',
        #         'serif': 'Computer Modern Roman',
        #         'weight': 'medium',
        #         'size': 1}
        # matplotlib.rc('font', **font)
        # matplotlib.rc('text', usetex=True)

        # ax1.legend(loc='upper left')
        ax1.set_xlabel('log(MC)')
        ax1.set_ylabel('RSSI')
        ax1.set_xlim(xmin=x_axis[0]-1, xmax=x_axis[-1]+1)

        ax2.set_xlabel('MC')
        ax2.set_ylabel('Packet loss (%)')
        ax2.set_xlim(xmin=x_axis[0]-1, xmax=x_axis[-1] + 10)
        ax2.set_ylim(200, 1000)

    #ax1.view_init(elev=elevation_angle, azim=azimuthal_angle)
    plt.savefig(cwd + "/figure/pdu200_delay" + delay[i] + "_br6_RSSI.eps", format='eps', dpi=1000)
    plt.show()

if __name__=="__main__":
    main()