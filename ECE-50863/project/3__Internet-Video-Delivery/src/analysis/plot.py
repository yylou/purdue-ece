import configparser
import glob
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

THROUGHPUT_HEADING  = 'throughput'

CHUNK_SIZE_RATIOS_HEADING   = 'chunk_size_ratios'
CHUNK_SIZE_RATIOS           = 'chunk_size_ratios'

table = {
    1: 'hi_avg_hi_var',
    2: 'hi_avg_mi_var',
    3: 'hi_avg_lo_var',
    4: 'mi_avg_hi_var',
    5: 'mi_avg_mi_var',
    6: 'mi_avg_lo_var',
    7: 'lo_avg_hi_var',
    8: 'lo_avg_mi_var',
    9: 'lo_avg_lo_var',
}

'''
Testing student algorithm 4
        Test hi_avg_hi_var.ini: Total Quality   395.00, Total Variation    32.00, Rebuffer Time     0.33, Total QoE     3.16
        Test hi_avg_mi_var.ini: Total Quality   414.00, Total Variation    24.00, Rebuffer Time     0.33, Total QoE     3.35
        Test hi_avg_lo_var.ini: Total Quality   388.00, Total Variation    30.00, Rebuffer Time     0.47, Total QoE     3.11
        Test mi_avg_hi_var.ini: Total Quality   257.00, Total Variation    57.00, Rebuffer Time     0.73, Total QoE     1.89
        Test mi_avg_mi_var.ini: Total Quality   199.00, Total Variation    48.00, Rebuffer Time     4.12, Total QoE     1.33
        Test mi_avg_lo_var.ini: Total Quality   247.00, Total Variation    50.00, Rebuffer Time     0.50, Total QoE     1.84
        Test lo_avg_hi_var.ini: Total Quality   155.00, Total Variation    68.00, Rebuffer Time     1.12, Total QoE     0.98
        Test lo_avg_mi_var.ini: Total Quality    84.00, Total Variation    68.00, Rebuffer Time     3.66, Total QoE     0.30
        Test lo_avg_lo_var.ini: Total Quality   112.00, Total Variation    40.00, Rebuffer Time    16.29, Total QoE     0.22

        Average QoE over all tests: 1.80
'''

#                      hi_avg_hi_var          hi_avg_mi_var          hi_avg_lo_var             mi_avg_hi_var          mi_avg_mi_var          mi_avg_lo_var             lo_avg_hi_var           lo_avg_mi_var         lo_avg_lo_var
RobustMPC           = [(401.00, 34.00, 0.33), (422.00, 30.00, 0.33), (392.00, 20.00, 0.47),    (264.00, 58.00, 3.90), (197.00, 36.00, 6.27), (259.00, 60.00, 3.30),    (152.00, 72.00, 11.04), (94.00, 54.00, 9.62), (115.00, 48.00, 20.40)]
#                     [3.20,                  3.39,                  3.18,                     1.84,                  1.29,                  1.81,                     0.60,                   0.24,                 0.08                  ] = 1.74
RobustMPC_var       = [(392.00, 26.00, 0.33), (410.00, 20.00, 0.33), (386.00, 20.00, 0.47),    (256.00, 39.00, 0.40), (198.00, 36.00, 3.93), (241.00, 38.00, 0.50),    (150.00, 64.00,  1.12), (71.00, 34.00, 1.08), ( 95.00, 31.00, 10.09)]
#                     [3.16,                  3.34,                  3.13,                     1.97,                  1.37,                  1.84,                     0.95,                   0.42,                 0.33                  ] = 1.83 
BBA2                = [(346.00, 14.00, 0.33), (371.00, 18.00, 0.33), (339.00, 28.00, 0.47),    (243.00, 39.00, 0.40), (181.00, 21.00, 4.05), (223.00, 31.00, 0.50),    (147.00, 27.00,  2.18), (65.00, 33.00, 3.27), (107.00, 25.00, 19.06)]
#                     [2.83,                  3.02,                  2.70,                     1.86,                  1.29,                  1.72,                     1.04,                   0.30,                 0.15                  ] = 1.66
BBA2_var            = [(395.00, 32.00, 0.33), (414.00, 24.00, 0.33), (388.00, 30.00, 0.47),    (257.00, 57.00, 0.73), (199.00, 48.00, 4.12), (247.00, 50.00, 0.50),    (155.00, 68.00,  1.12), (84.00, 68.00, 3.66), (112.00, 40.00, 16.29)]
#                     [3.16,                  3.35,                  3.11,                     1.89,                  1.33,                  1.84,                     0.98,                   0.30,                 0.22                  ] = 1.80

def plot_throughput(config_path):
    data_throughput = {}

    for k, v in config_path.items():
        cfg = configparser.RawConfigParser(allow_no_value=True, inline_comment_prefixes='#')
        cfg.read(v)

        throughputs = dict(cfg.items(THROUGHPUT_HEADING))
        throughputs = [(float(time), float(throughput)) for time, throughput in throughputs.items()]

        data_throughput[k] = throughputs

    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(12, 12))
    fig.tight_layout(h_pad=5)

    counter = 1
    for row in ax:
        for col in row:
            col.plot(*zip(*data_throughput[table[counter]]))
            col.set_title(table[counter])
            counter += 1

    plt.show()

def plot_chunk_size_ratios(config_path):
    data_chunk_size_ratios = {}

    for k, v in config_path.items():
        cfg = configparser.RawConfigParser(allow_no_value=True, inline_comment_prefixes='#')
        cfg.read(v)

        chunks = cfg.get(CHUNK_SIZE_RATIOS_HEADING, CHUNK_SIZE_RATIOS)
        chunks = list(float(x) for x in chunks.split(',') if x.strip())

        data_chunk_size_ratios[k] = chunks

    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(12, 12))
    fig.tight_layout(h_pad=5)

    counter = 1
    for row in ax:
        for col in row:
            col.plot(data_chunk_size_ratios[table[counter]])
            col.set_title(table[counter])
            counter += 1

    plt.show()

def calculate_QoE(data: list[tuple], option='ALL') -> list[float]:
    if option == 'ALL': return [round((element[0] * 2 + element[1] * -1 + element[2] * -8) / 239., 2) for element in data]
    if option ==     1: return [round((element[0] *  2) / 239., 2) for element in data]
    if option ==     2: return [round((element[1] * -1) / 239., 2) for element in data]
    if option ==     3: return [round((element[2] * -8) / 239., 2) for element in data]

def compare(option='ALL'):
    QoE_RobustMPC       = calculate_QoE(RobustMPC, option)
    QoE_RobustMPC_var   = calculate_QoE(RobustMPC_var, option)
    QoE_BBA2            = calculate_QoE(BBA2, option)
    QoE_BBA2_var        = calculate_QoE(BBA2_var, option)

    fig = plt.figure(figsize=(12, 12))
    fig.subplots_adjust(left=0.07, bottom=0.07, right=0.77, top=0.88, wspace=0.4, hspace=0.2)

    for i in range(1, 10):
        # Plot Settings
        ax = fig.add_subplot(3, 3, i)
        plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)
        
        # Data
        x = [1, 2, 3, 4]
        y = [QoE_RobustMPC[i-1], QoE_RobustMPC_var[i-1], QoE_BBA2[i-1], QoE_BBA2_var[i-1]]
        plt.bar(x, y, color=['C0', 'C1', 'C2', 'C3'])

        # Text
        for k, v in enumerate(y): ax.text(k+0.7 if v > 0 else k+0.65, v if v > 0 else v, f'{v:.2f}', color='black', fontweight='bold', fontsize=9)

        # Title
        plt.title(table[i])

        # Label
        if option == 'ALL': plt.ylabel('Composite QoE Score')
        if option ==     1: plt.ylabel('Quality Variation QoE Score')
        if option ==     2: plt.ylabel('Total Quality QoE Score')
        if option ==     3: plt.ylabel('Rebuffer Time QoE Score')

        # Ticks
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off

    # Global Title
    if option ==  'ALL': fig.suptitle('Composite QoE Score of Different Algorithms in Each Trace',          fontsize=14, fontweight='bold', y=0.95)
    if option ==      1: fig.suptitle('Total Quality QoE Score of Different Algorithms in Each Trace',      fontsize=14, fontweight='bold', y=0.95)
    if option ==      2: fig.suptitle('Quality Variation QoE Score of Different Algorithms in Each Trace',  fontsize=14, fontweight='bold', y=0.95)
    if option ==      3: fig.suptitle('Rebuffer Time QoE Score of Different Algorithms in Each Trace',      fontsize=14, fontweight='bold', y=0.95)

    # Legend
    bar = [
            mpatches.Patch(facecolor='C0', label='RobustMPC'),
            mpatches.Patch(facecolor='C1', label='RobustMPC Variant'),
            mpatches.Patch(facecolor='C2', label='BBA-2'),
            mpatches.Patch(facecolor='C3', label='BBA-2 Variant')
        ]
    legend = plt.legend(handles=bar, loc='center left', bbox_to_anchor=(1.2, 1.7), borderaxespad=0., fancybox=True)
    legend.set_title(title='ABR Algorithms', prop={'weight': 'bold'})
    ax.add_artist(legend)

    plt.plot()

def plot_composite():
    fig, ax = plt.subplots(figsize=(9, 9))
    plt.subplots_adjust(left=0.09, bottom=0.16, right=0.7, top=0.95, wspace=0.2, hspace=0.2)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)

    QoE_base    = calculate_QoE(BBA2)
    QoE_variant = calculate_QoE(BBA2_var)

    x1 = [1,    2,    3,    4,    5,    6,    7,    8,    9]
    x2 = [1.45, 2.45, 3.45, 4.45, 5.45, 6.45, 7.45, 8.45, 9.45]
    y1 = [round(QoE_base[i], 2)    for i in range(9)]
    y2 = [round(QoE_variant[i], 2) for i in range(9)]

    plt.bar(x1,  y1, width=0.4, color='C0')
    plt.bar(x2,  y2, width=0.4, color='C1')

    for i, v in enumerate(y1): ax.text(i+0.63, v+0.02 if v > 0 else v-0.08, f'{v:.2f}', color='C0', fontweight='bold')
    for i, v in enumerate(y2): ax.text(i+1.23, v+0.02 if v > 0 else v-0.08, f'{v:.2f}', color='C1', fontweight='bold')

    plt.title('Composite QoE Score of Different Traces vs. Different Algorithm')
    plt.ylabel('Composite QoE Score')
    ax.set_xticks([1.225, 2.225, 3.225, 4.225, 5.225, 6.225, 7.225, 8.225, 9.225])
    ax.set_xticklabels(table.values(), rotation='vertical')

    bar1 = mpatches.Patch(facecolor='C0', label='Composite QoE Score')
    legend1 = plt.legend(handles=[bar1], loc='center left', bbox_to_anchor=(1.05, 0.6), borderaxespad=0., fancybox=True)
    bar1 = mpatches.Patch(facecolor='C1', label='Composite QoE Score')
    legend2 = plt.legend(handles=[bar1], loc='center left', bbox_to_anchor=(1.05, 0.4), borderaxespad=0., fancybox=True)
    
    legend1.set_title(title="BBA-2",   prop={'weight': 'bold'})
    legend2.set_title(title="Variant", prop={'weight': 'bold'})

    ax.add_artist(legend1)
    ax.add_artist(legend2)
    
    plt.tick_params(
        axis='x',     # changes apply to the x-axis
        which='both', # both major and minor ticks are affected
        bottom=False  # ticks along the bottom edge are off
    )

    plt.plot()

def plot_individual_hi_traces():
    fig, ax = plt.subplots(figsize=(9, 9))
    plt.subplots_adjust(left=0.09, bottom=0.05, right=0.75, top=0.95, wspace=0.2, hspace=0.2)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)

    x  = [1,    2,    3]
    x1 = [1.45, 2.45, 3.45]
    y1 = [round(calculate_QoE(BBA2, 1)[i], 2)     for i in range(3)]
    y2 = [round(calculate_QoE(BBA2, 2)[i], 2)     for i in range(3)]
    y3 = [round(calculate_QoE(BBA2, 3)[i], 2)     for i in range(3)]
    y4 = [round(calculate_QoE(BBA2_var, 1)[i], 2) for i in range(3)]
    y5 = [round(calculate_QoE(BBA2_var, 2)[i], 2) for i in range(3)]
    y6 = [round(calculate_QoE(BBA2_var, 3)[i], 2) for i in range(3)]

    bar_width = 0.4

    plt.bar(x,  y1, width=bar_width,            color='C0')
    plt.bar(x,  y2, width=bar_width, bottom=0,  color='C1')
    plt.bar(x,  y3, width=bar_width, bottom=y2, color='C4')

    for i, v in enumerate(y1):  ax.text(i+0.91, v+0.02,               f'{v:.2f}', color='C0', fontweight='bold')
    for i, v in enumerate(y2):  ax.text(i+0.91, 0.02,                 f'{v:.2f}', color='C1', fontweight='bold')
    for i, v in enumerate(y3):  ax.text(i+0.91, (y2[i] + y3[i])-0.07, f'{v:.2f}', color='C4', fontweight='bold')

    plt.bar(x1, y4, width=bar_width,            color='C0', hatch='\\\\\\')
    plt.bar(x1, y5, width=bar_width, bottom=0,  color='C1', hatch='////')
    plt.bar(x1, y6, width=bar_width, bottom=y5, color='C2')
    for i, v in enumerate(y4):  ax.text(i+1.36, v+0.02,               f'{v:.2f}', color='C0', fontweight='bold')
    for i, v in enumerate(y5):  ax.text(i+1.36, 0.02,                 f'{v:.2f}', color='C1', fontweight='bold')
    for i, v in enumerate(y6):  ax.text(i+1.36, (y5[i] + y6[i])-0.07, f'{v:.2f}', color='C2', fontweight='bold')

    plt.title('QoE of Different Traces vs. Different Algorithm')
    plt.ylabel('QoE Score')
    ax.set_xticks([1.225, 2.225, 3.225])
    ax.set_xticklabels([table[i] for i in range(1, 4)])
    
    bar1 = mpatches.Patch(facecolor='C0', label='Total Quality')
    bar2 = mpatches.Patch(facecolor='C1', label='Quality Variation')
    bar3 = mpatches.Patch(facecolor='C4', label='Rebuffer Time')
    legend1 = plt.legend(handles=[bar1, bar2, bar3], loc='center left', bbox_to_anchor=(1.05, 0.6), borderaxespad=0., fancybox=True)

    bar1 = mpatches.Patch(facecolor='C0', label='Total Quality',        hatch='\\\\\\')
    bar2 = mpatches.Patch(facecolor='C1', label='Quality Variation',    hatch='////')
    bar3 = mpatches.Patch(facecolor='C2', label='Rebuffer Time')
    legend2 = plt.legend(handles=[bar1, bar2, bar3], loc='center left', bbox_to_anchor=(1.05, 0.4), borderaxespad=0., fancybox=True)
    
    legend1.set_title(title="BBA-2",   prop={'weight': 'bold'})
    legend2.set_title(title="Variant", prop={'weight': 'bold'})

    ax.add_artist(legend1)
    ax.add_artist(legend2)
    
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
    )

    plt.plot()

def plot_individual_mi_lo_traces():
    fig, ax = plt.subplots(figsize=(9, 9))
    plt.subplots_adjust(left=0.09, bottom=0.14, right=0.75, top=0.95, wspace=0.2, hspace=0.2)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)

    x  = [1,    2,    3,    4,      5,      6]
    x1 = [1.45, 2.45, 3.45, 4.45,   5.45,   6.45]
    y1 = [round(calculate_QoE(BBA2, 1)[i], 2)     for i in range(3, 9)]
    y2 = [round(calculate_QoE(BBA2, 2)[i], 2)     for i in range(3, 9)]
    y3 = [round(calculate_QoE(BBA2, 3)[i], 2)     for i in range(3, 9)]
    y4 = [round(calculate_QoE(BBA2_var, 1)[i], 2) for i in range(3, 9)]
    y5 = [round(calculate_QoE(BBA2_var, 2)[i], 2) for i in range(3, 9)]
    y6 = [round(calculate_QoE(BBA2_var, 3)[i], 2) for i in range(3, 9)]

    bar_width = 0.4

    plt.bar(x,  y1, width=bar_width,            color='C0')
    plt.bar(x,  y2, width=bar_width, bottom=0,  color='C1')
    plt.bar(x,  y3, width=bar_width, bottom=y2, color='C4')

    for i, v in enumerate(y1):  ax.text(i+0.79, v+0.02,               f'{v:.2f}', color='C0', fontweight='bold')
    for i, v in enumerate(y2):  ax.text(i+0.79, 0.02,                 f'{v:.2f}', color='C1', fontweight='bold')
    for i, v in enumerate(y3):  ax.text(i+0.79, (y2[i] + y3[i])-0.07, f'{v:.2f}', color='C4', fontweight='bold')

    plt.bar(x1, y4, width=bar_width,            color='C0', hatch='\\\\\\')
    plt.bar(x1, y5, width=bar_width, bottom=0,  color='C1', hatch='////')
    plt.bar(x1, y6, width=bar_width, bottom=y5, color='C2')
    for i, v in enumerate(y4):  ax.text(i+1.24, v+0.02,               f'{v:.2f}', color='C0', fontweight='bold')
    for i, v in enumerate(y5):  ax.text(i+1.24, 0.02,                 f'{v:.2f}', color='C1', fontweight='bold')
    for i, v in enumerate(y6):  ax.text(i+1.24, (y5[i] + y6[i])-0.07, f'{v:.2f}', color='C2', fontweight='bold')

    plt.title('QoE of Different Traces vs. Different Algorithm')
    plt.ylabel('QoE Score')
    ax.set_xticks([1.225, 2.225, 3.225, 4.225, 5.225, 6.225])
    ax.set_xticklabels([table[i] for i in range(4, 10)], rotation=90)
    
    bar1 = mpatches.Patch(facecolor='C0', label='Total Quality')
    bar2 = mpatches.Patch(facecolor='C1', label='Quality Variation')
    bar3 = mpatches.Patch(facecolor='C4', label='Rebuffer Time')
    legend1 = plt.legend(handles=[bar1, bar2, bar3], loc='center left', bbox_to_anchor=(1.05, 0.6), borderaxespad=0., fancybox=True)

    bar1 = mpatches.Patch(facecolor='C0', label='Total Quality',        hatch='\\\\\\')
    bar2 = mpatches.Patch(facecolor='C1', label='Quality Variation',    hatch='////')
    bar3 = mpatches.Patch(facecolor='C2', label='Rebuffer Time')
    legend2 = plt.legend(handles=[bar1, bar2, bar3], loc='center left', bbox_to_anchor=(1.05, 0.4), borderaxespad=0., fancybox=True)
    
    legend1.set_title(title="BBA-2",   prop={'weight': 'bold'})
    legend2.set_title(title="Variant", prop={'weight': 'bold'})

    ax.add_artist(legend1)
    ax.add_artist(legend2)
    
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
    )

    plt.plot()

def main():
    configs, config_path = glob.glob('./tests/*.ini'), {}
    for config in configs:
        config_path[config.split('/')[-1].split('.')[0]] = config

    """
    Plot Test Configurations
    """
    # plot_throughput(config_path)
    # plot_chunk_size_ratios(config_path)

    """
    All Algorithms and Variants Comparison
    """
    compare()
    compare(1)
    compare(2)
    compare(3)

    """
    Plot QoE Score Comparison: Composite QoE Score
    """
    plot_composite()

    """
    Plot QoE Score Comparison: Invidual QoE Score
    """
    plot_individual_hi_traces()
    plot_individual_mi_lo_traces()

    plt.show()

if __name__ == '__main__':
    main()
