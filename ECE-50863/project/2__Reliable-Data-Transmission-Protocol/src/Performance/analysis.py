#!/usr/bin/env python3
#
#    Author : Yuan-Yao Lou (Mike) <yylou@purdue.edu>
#    Title  : Ph.D. student in ECE at Purdue University
#    Date   : 2021/10/25
#


import glob as GLOB
import os as OS
import sys as SYS
import matplotlib
import matplotlib.pyplot as PLOT


def parse(PATH, debug=False):
    goodput, overhead, correctness = {}, {}, {}
    FILES = GLOB.glob(f'{PATH}/*')

    for FILE in FILES:
        TIMESTAMP = FILE.split('/')[1].split('-', maxsplit=1)[1].replace('.log', '')

        with open(FILE, 'r') as F:
            for line in F.readlines():
                if   'Goodput'  in line: goodput[TIMESTAMP]  = float(line.split()[-2])
                elif 'Overhead' in line: overhead[TIMESTAMP] = float(line.split()[-2])
                elif 'File transmission correct' in line: correctness[TIMESTAMP] = line.split()[-1]

    # Log File Consistency Check
    if debug:
        for TIMESTAMP in goodput.keys():
            print(f'{TIMESTAMP}: Goodput: {goodput[TIMESTAMP]:>10}, Overhead: {overhead[TIMESTAMP]:>10}, Correctness: {correctness[TIMESTAMP]}')
        print()

    return goodput, overhead, correctness

def main():
    # Simple Argument Handling
    if len(SYS.argv) < 2: 
        print('Usage: python3 plot.py <LOG_FOLDER_PATH>')

    # Parse Log File
    goodput, overhead, correctness = parse(SYS.argv[1])

    # Sort by 'Goodput'
    sort_by_goodput  = sorted(goodput.items(), key=lambda item: item[1])
    sort_by_overhead = sorted(overhead.items(), key=lambda item: item[1], reverse=True)
    for k, v in sort_by_goodput:
        print(f'{k}: Goodput: {goodput[k]:>10.2f}, Overhead: {overhead[k]:>10}, Correctness: {correctness[k]}')
    print()
    # Sort by 'Overhead
    for k, v in sort_by_overhead:
        print(f'{k}: Goodput: {goodput[k]:>10.2f}, Overhead: {overhead[k]:>10}, Correctness: {correctness[k]}')

    # Plot
    fig1, ax1 = PLOT.subplots()
    ax1.set_title('Goodput / Overhead')
    data = ax1.boxplot([[_[1] for _ in sort_by_goodput], [_[1] for _ in sort_by_overhead]])
    
    # Annotate Text
    for line in data['medians']:
        x, y = line.get_xydata()[1]
        PLOT.text(x, y, '%.2f' % y, color='blue')

    # for line in data['boxes']:
    #     x, y = line.get_xydata()[0]
    #     PLOT.text(x, y, '%.2f' % y, color='blue')
        
    #     x, y = line.get_xydata()[3]
    #     PLOT.text(x, y, '%.2f' % y, color='blue')
    
    # for line in data['caps']:
    #     x, y = line.get_xydata()[0]
    #     PLOT.text(x, y, '%.2f' % y, color='blue')  
    
    print(f'#Data: {len(goodput)}, {len(overhead)}')

    PLOT.xticks([1, 2], ['Goodput', 'Overhead'])
    PLOT.show()

if __name__ == '__main__':
    main()