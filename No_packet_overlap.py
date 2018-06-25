import os
import pyshark

import matplotlib
from matplotlib.legend_handler import HandlerErrorbar

import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

def read_file(filepath, rvid):
    num_rec = 0
    RSSI = []
    cap = pyshark.FileCapture(filepath)
    for pkt in cap:
        try:
            if (pkt.wlan.sa == rvid):
                num_rec += 1
                RSSI.append(int(pkt.wlan_radio.signal_dbm))
        except:
            continue

    RSSI_mean = sum(RSSI) / len(RSSI)
    z_critical = stats.norm.ppf(q=0.975)  # Get the z-critical value*
    RSSI_std = np.std(RSSI)
    margin_of_error = z_critical * (RSSI_std / np.sqrt(len(RSSI)))
    interval = (RSSI_mean - margin_of_error, RSSI_mean + margin_of_error)
    RSSI_confidence_interval[i].append(interval)
    print(RSSI_mean, RSSI_confidence_interval)
    return (num_rec, RSSI_mean, RSSI_confidence_interval)


fig1, ax1 = plt.subplots(figsize=(5, 4))
fig2, ax2 = plt.subplots(figsize=(5, 4))

cwd = os.getcwd()

delay = ["9k"]
MC = [1, 5, 10, 100, 500, 600, 700, 800]

num_rec = []
RSSI = []
RSSI_mean = []
RSSI_confidence_interval = []

for i in range(0, len(delay)):
    num_rec.append([])
    RSSI.append([])
    RSSI_mean.append([])
    RSSI_confidence_interval.append([])
    for j in range(0, len(MC)):
        RSSI = []
        num_rec[i].append(0)
        cap = pyshark.FileCapture(cwd + "/Data/pdu200_delay" + delay[i] + "_MC" + str(MC[j]) + "m" + str(MC[j]) + "m" + "_br6.pcapng")

        for pkt in cap:
            try:
                if (pkt.wlan.sa == "23:23:23:23:23:23"):
                    num_rec[i][j] += 1
                    RSSI.append(int(pkt.wlan_radio.signal_dbm))
            except:
                continue

        RSSI_mean[i].append(sum(RSSI) / len(RSSI))
        z_critical = stats.norm.ppf(q=0.975)  # Get the z-critical value*
        RSSI_std = np.std(RSSI)
        margin_of_error = z_critical * (RSSI_std / np.sqrt(len(RSSI)))
        interval = (RSSI_mean[i][j] - margin_of_error, RSSI_mean[i][j] + margin_of_error)
        RSSI_confidence_interval[i].append(interval)
        print(RSSI_mean[i][j], RSSI_confidence_interval[i][j])



    ax1.errorbar(x=MC,
                 y=RSSI_mean[i],
                 yerr=[(top - bot) / 2 for top, bot in RSSI_confidence_interval[i]],
                 fmt='o')
                 # label='$MC1=0.5$')

    ax2.plot(x=MC,
             y=num_rec[i])

    # font = {'family': 'serif',
    #         'serif': 'Computer Modern Roman',
    #         'weight': 'medium',
    #         'size': 1}
    # matplotlib.rc('font', **font)
    # matplotlib.rc('text', usetex=True)

    # ax1.legend(loc='upper left')
    ax1.set_xlabel('MC')
    ax1.set_ylabel('RSSI')
    ax1.set_xlim(xmin=0, xmax=MC[-1]+10)


#ax1.view_init(elev=elevation_angle, azim=azimuthal_angle)
plt.savefig(cwd + "/figure/pdu200_delay" + delay[i] + "_br6_RSSI.eps", format='eps', dpi=1000)
plt.show()