import matplotlib.pyplot as plt
import numpy as np

colors = ['C1', 'C2', 'C3', 'C4', 'C5']
labels = [r'Srv1', r'Srv2']

def make_plot(infiles, outfile):
    data_files=infiles
    normalized_data = []
    for f in data_files:
        data = np.loadtxt(f)
        sum_f = np.sum(data[:, 1])# sum of values
        inter = data[2, 0] # inter-bin itnerval
        norm_factor = 1.0 / (sum_f * inter)
        normalized_data.append((data, norm_factor))
    plt.figure(figsize=(10, 6))
    for i, (data, norm_factor) in enumerate(normalized_data):
        x = data[:, 0]
        y = data[:, 1] * norm_factor
        plt.plot(x, y, label=labels[i], color=colors[i % len(colors)])
    plt.xlabel('Response Time [s]', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend(loc='upper right')
    plt.savefig(outfile, dpi=300, bbox_inches='tight')

make_plot(['analisi/histogram.data'], 'histogram.png')