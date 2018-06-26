import os
from os.path import dirname
import pyshark

import matplotlib
from matplotlib.legend_handler import HandlerErrorbar

import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

# def fig_configure():
#     font = {'family': 'serif',
#             'serif': 'Computer Modern Roman',
#             'weight': 'medium',
#             'size': 1}
#     matplotlib.rc('font', **font)
#     matplotlib.rc('text', usetex=True)
#     # ax1.view_init(elev=elevation_angle, azim=azimuthal_angle)
#     return 0


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

def errorbar_plot(ax, n, _x, _y, _ci): #_ci: confidence interval
    nz_x = []
    nz_y = []
    nz_err = []

    # ignore the part of num_rv[i]=0
    for i in range(len(n)):
        print(n[i])
        if (n[i]):
            nz_x.append(_x[i])
            nz_y.append(_y[i])
            nz_err.append((_ci[i][0] - _ci[i][1]) / 2)
    ax.errorbar(x = nz_x,
                y = nz_y,
                yerr = nz_err,
                fmt='o')
    ax.plot(nz_x, nz_y,
            c=(0.25, 0.25, 1.00),
            lw=1,
            zorder=10)
    ax.set_xlabel('MC')
    ax.set_xscale('log')
    ax.set_ylabel('RSSI')
    ax.set_xlim(xmin=_x[0], xmax=_x[-1])
    return 0

def line_plot(ax, _x, _y):
    ax.plot(_x, _y,
            lw=1,
            zorder=10,
            marker = 'o')
    ax.set_xlabel('MC')
    ax.set_xscale('log')
    ax.set_ylabel('Packet loss (%)')
    ax.set_xlim(xmin=_x[0], xmax=_x[-1])