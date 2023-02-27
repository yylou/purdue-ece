#
#    Author : Yuan-Yao Lou (Mike) <yylou@purdue.edu>
#    Title  : Ph.D. student in ECE at Purdue University
#    Date   : 2021/10/27
#


import glob as GLOB
import numpy as NP
import sys as SYS
import matplotlib
import matplotlib.pyplot as PLOT


def main():
    PATH      = {'1': 'wnd_10_v2',  '2': 'wnd_20_v2',   '3': 'wnd_30_v2',   '4': 'wnd_40_v2',   '5': 'wnd_50_v2'}
    goodput   = {'1': [],           '2': [],            '3': [],            '4': [],            '5': []}
    overhead  = {'1': [],           '2': [],            '3': [],            '4': [],            '5': []}
    mean_g    = {'1': 0,            '2': 0,             '3': 0,             '4': 0,             '5': 0}
    error_g   = {'1': 0,            '2': 0,             '3': 0,             '4': 0,             '5': 0}
    mean_o    = {'1': 0,            '2': 0,             '3': 0,             '4': 0,             '5': 0}
    error_o   = {'1': 0,            '2': 0,             '3': 0,             '4': 0,             '5': 0}

    for k, v in PATH.items():
        for FILE in GLOB.glob(f'{v}/*'):
            with open(FILE, 'r') as F:
                for line in F.readlines():
                    if   'Goodput'  in line: goodput[k].append(float(line.split()[-2]))
                    elif 'Overhead' in line: overhead[k].append(float(line.split()[-2]))

    for k, v in PATH.items():
        goodput[k]  = goodput[k]
        mean_g[k]   = NP.mean(goodput[k])
        error_g[k]  = NP.std(goodput[k])
        
        overhead[k] = overhead[k]
        mean_o[k]   = NP.mean(overhead[k])
        error_o[k]  = NP.std(overhead[k])

    # ========================================
    #   Goodput                              =
    # ========================================

    # Figure information
    PLOT.figure()
    ax = PLOT.gca()
    PLOT.title('Goodput vs. Different Window Size')
    PLOT.xlabel('Window Size')
    PLOT.ylabel('Goodpput (bytes/sec)')

    # Grid / Axis setting
    PLOT.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)
    PLOT.ylim(0, max(mean_g.values()) + max(error_g.values()) * 2)

    # Add bar
    PLOT.bar(0.1, mean_g['1'], yerr=error_g['1'],   width=0.1, capsize=5)
    PLOT.bar(0.3, mean_g['2'], yerr=error_g['2'],   width=0.1, capsize=5)
    PLOT.bar(0.5, mean_g['3'], yerr=error_g['3'],   width=0.1, capsize=5)
    PLOT.bar(0.7, mean_g['4'], yerr=error_g['4'],   width=0.1, capsize=5)
    PLOT.bar(0.9, mean_g['5'], yerr=error_g['5'],   width=0.1, capsize=5)

    ax.text(0.1, mean_g['1'], f"{mean_g['1']:.2f}",  ha='center')
    ax.text(0.3, mean_g['2'], f"{mean_g['2']:.2f}",  ha='center')
    ax.text(0.5, mean_g['3'], f"{mean_g['3']:.2f}",  ha='center')
    ax.text(0.7, mean_g['4'], f"{mean_g['4']:.2f}",  ha='center')
    ax.text(0.9, mean_g['5'], f"{mean_g['5']:.2f}",  ha='center')

    # Hide X tick
    ax.axes.xaxis.set_ticklabels([])
    PLOT.tick_params(axis="x", bottom=False)

    # Legend
    PLOT.legend([
            'wnd=10', 
            'wnd=20', 
            'wnd=30', 
            'wnd=40', 
            'wnd=50'], 
            loc='lower right'
        )

    # PLOT.show()

    # ========================================
    #   Overhead                             =
    # ========================================

    # Figure information
    PLOT.figure()
    ax = PLOT.gca()
    PLOT.title('Overhead vs. Different Window Size')
    PLOT.xlabel('Window Size')
    PLOT.ylabel('Overhead (bytes)')

    # Grid / Axis setting
    PLOT.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)
    PLOT.ylim(0, max(mean_o.values()) + max(error_o.values()) * 1.2)

    # Add bar
    PLOT.bar(0.1, mean_o['1'], yerr=error_o['1'], width=0.1, capsize=5)
    PLOT.bar(0.3, mean_o['2'], yerr=error_o['2'], width=0.1, capsize=5)
    PLOT.bar(0.5, mean_o['3'], yerr=error_o['3'], width=0.1, capsize=5)
    PLOT.bar(0.7, mean_o['4'], yerr=error_o['4'], width=0.1, capsize=5)
    PLOT.bar(0.9, mean_o['5'], yerr=error_o['5'], width=0.1, capsize=5)

    ax.text(0.1, mean_o['1'], f"{mean_o['1']:.2f}", ha='center')
    ax.text(0.3, mean_o['2'], f"{mean_o['2']:.2f}", ha='center')
    ax.text(0.5, mean_o['3'], f"{mean_o['3']:.2f}", ha='center')
    ax.text(0.7, mean_o['4'], f"{mean_o['4']:.2f}", ha='center')
    ax.text(0.9, mean_o['5'], f"{mean_o['5']:.2f}", ha='center')

    # Hide X tick
    ax.axes.xaxis.set_ticklabels([])
    PLOT.tick_params(axis="x", bottom=False)

    # Legend
    PLOT.legend([
            'wnd=10', 
            'wnd=20', 
            'wnd=30', 
            'wnd=40', 
            'wnd=50'], 
            loc='lower right'
        )

    PLOT.show()

if __name__ == '__main__':
    main()