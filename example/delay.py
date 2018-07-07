import os
import sys
from os.path import dirname
from math import *
import matplotlib.pyplot as plt

sys.path.append("../src/")
from figure_plot import *

def main():
    fig2, ax2 = plt.subplots(figsize=(5, 4)) #fig2: packet loss to multiple constant


    cwd = os.getcwd()

    delay = ["-20", "-10", "0", "10", "20", "30","40","50","60","70", "160"]
    delay_val = [-10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 80]
    MC = [50]
    # SIR = [10*log10(500/i) for i in MC]
    MC_str = ['50m']

    num_rv = [[0] * len(delay) for i in range(len(MC))]
    rssi_mean = [[0] * len(delay) for i in range(len(MC))]
    rssi_confidence_interval = [[0] * len(delay) for i in range(len(MC))]
    packet_loss = [[1.0] * len(delay) for i in range(len(MC))]

    for i in range(0, len(MC)):
        for j in range(0, len(delay)):
            file_path = dirname(cwd) + "/data/pdu200_delay" + delay[j] + "_MC500m" + MC_str[i] + "_br6.pcapng"
            rv_id = "23:23:23:23:23:23"
            num_rv[i][j], rssi_mean[i][j], rssi_confidence_interval[i][j] = read_file(file_path, rv_id)
            packet_loss[i][j] = (1000 - num_rv[i][j]) / 1000


    # plot RSSI to multiple constant
    ax2.plot(delay_val, packet_loss[0],
            lw=1,
            zorder=10,
            marker='s',
            linestyle = '-')

    ax2.set_xlabel('Delay time ($\mu s$)')
    # ax2.set_xscale('log')
    ax2.set_ylabel('Packet loss (100%)')
    # ax2.set_xlim(xmin=0, xmax=100)

    # fig1.gca().legend(('$\Delta t = -4 us$', '$\Delta t = \pm 0 us$', '$\Delta t = +4 us$'))
    # fig2.gca().legend(('$\Delta t = -8 us$, packet', '$\Delta t = -8 us$, noise', '$\Delta t = +8 us$, packet', '$\Delta t = +8 us$, noise'))
    # fig1.tight_layout()
    fig2.tight_layout()

        # save figures
    # fig1.savefig(dirname(cwd) + "/figure/pdu200_diff_delay_br6_RSSI.eps", format='eps', dpi=1000)
    fig2.savefig(dirname(cwd) + "/figure/pdu200_diff_delay_br6_Packetloss.eps", format='eps', dpi=1000)

    return 0

if __name__=="__main__":
    main()
    plt.show()