#!/usr/bin/python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
import matplotlib as mpl
import matplotlib.colors as mc
from plots import plot_line, set_fonts

mu=100
lam=10
ts=0.1
delta=0.1
def theoretical(x):
    return 1/10 * (2*x**2 - 2 * x + 1) / ((1 - x) * x) + (1 - x) * 0.07
    

if __name__ == "__main__":
    #set_fonts()
    # plot response time
    fig, ax = plt.subplots()
    ax.set(xlabel='$x$', ylabel='Time [s]')
    plot_line(ax, 'o--', 'analisi/es3.data', 'Response Time', '#p', 'ResponseTime', 'sigma(ResponseTime)')
    pts=[x/10.0 for x in range(1, 10)]
    plot_line(ax, '-', None, 'Theoretical Curve', pts, [theoretical(x) for x in pts])
    plt.legend()
    plt.savefig('sample.png')
    plt.show()

