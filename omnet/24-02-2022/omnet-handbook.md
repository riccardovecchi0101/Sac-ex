# Omnet

## Setup python environment
```sh
source source ../omnetpp-6.3.0/setenv
```

## Definisci la rete
Crea un file `.ned` con la seguente struttura:
```
import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Router;

network net_name // CHANGE_ME
{
    parameters:
        double lambda = default(10);
        double mu = default(10);

        src.interArrivalTime = 1.0s * exponential(1 / lambda);
        srv.serviceTime = 1.0s * exponential(1 / mu);

    submodules:
        router: Router;
        src: Source;
        srv: Queue;
        sink: Sink;

    connections:
        src.out --> router.in++;
        router.out++ --> srv.in++;
        srv.out --> sink.in++;
}
```
Le classi usate sopra sono definite in `../omnetpp-6.3.0/samples/queueinglib`.  
**Distribuzioni**: variabili avente keyword `volatile`.  
- `exponential(mean)`
- `normal(mean, std_dev)`
- `truncormal(mean, std_dev)`
- `lognormal(mean, std_dev)` (i parametri della lognormal vanno calcolati in base alle formule su [wiki](https://en.wikipedia.org/wiki/Log-normal_distribution#Generation_and_parameters), puoi usare le [operazioni matematiche di omnet++](https://doc.omnetpp.org/omnetpp5/manual/#sec:ned-functions:category-math))
    - `1.0s*lognormal(log(1.0/(mu*sqrt(1+cv^2))), sqrt(log(1+cv^2)))`
- ... [more](https://doc.omnetpp.org/omnetpp5/manual/#sec:sim-lib:random-variate-generation)  

**Unità di misura**: puoi definire una variabile con unità di misura in questo modo  
`double a @unit(s) = ...`

**Array e for**: è possibile definire array di qualsiasi elemento della rete
```
int N = default(10);
srv[N]: Queue;
```
Puoi usare wildcard o cicli for per riferirti ad ognuno di essi.
```
srv[*]

for i=1..N-1 {
    srv[i]...
}
```

## Definisci la simulazione
Scrivi un file `.ini.mako` col seguente contenuto:
```
[General]
ned-path = .;../omnetpp-6.3.0/samples/queueinglib
network = net-name
cmdenv-config-name = net-name_Base
qtenv-default-config = net-name_Base

repeat = 5
sim-time-limit = 10000s
cpu-time-limit = 60s
**.vector-recording = false

[Config net-name_Base]
description = "Global scenario"
**.sink.lifeTime.result-recording-modes = +histogram
%for rho in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:

[Config net-name_rho${"%02d" % int(rho*10)}]
extends = net-name_Base
**.rho = ${rho}
%endfor
```
Per applicare il template usa:
```sh
update_template.py -t template.ini.mako
```

## Lancia la simulazione
Definisci uno script di esecuzione `run`:
```sh
#!/bin/sh
opp_run -l $(dirname $0)/../omnetpp-6.3.0/samples/queueinglib/queueinglib $*
```
```sh
chmod u+x ./run
```
Per eseguire la simulazione in modo grafico esegui.
```sh
unset GTK_PATH
./run template.ini
```
Per eseguire la simulazione in modo automatizzato svolgi i passi seguenti:
1. Crea il `Runfile`
```sh
make_runfile.py -f template.ini
```
2. Esegui la simulazione
```sh
make -j $(nproc) -f Runfile
```

## Raccolta e analisi dati
Definisci la configurazione di raccolta dati `config.json`.
```json
{
    "scenario_schema": {
        "rho": {"pattern": "**.rho", "type": "real"}
    },
    "metrics": {
        "ResponseTime": {"module": "**.sink", "scalar_name": "lifeTime:mean" ,"aggr": ["none"]}
    },
    "histograms": {
        "ResponseTimeHistogram": {"module": "**.sink", "histogram_name": "lifeTime:histogram"}
    },
    "analyses": {
        "Hist_RT": {
            "outfile": "results/histogram.data",
            "scenario": {"rho": "0.7"},
            "histogram": "ResponseTimeHistogram"
        },
        "Sens-rho": {
            "outfile": "results/ResponseTime-rho.data",
            "scenarios": {
                "fixed": { "key": "value" },
                "range": ["rho"]
            },
            "metrics": [
                {"metric": "ResponseTime", "aggr": "none"}
                    ]
        }
    }
}
```

**Metriche comuni**:
```json
"DroppedJobs": {"module": "**.srv", "scalar_name": "dropped:count" ,"aggr": ["none"]},
"QLen": {"module": "**.srv", "scalar_name": "queueLength:timeavg" ,"aggr": ["none"]},
"Utilization": {"module": "**.srv", "scalar_name": "busy:timeavg" ,"aggr": ["none"]},
"ServiceTime": {"module": "**.sink", "scalar_name": "totalServiceTime:mean" ,"aggr": ["none"]},
"WaitingTime": {"module": "**.sink", "scalar_name": "totalQueueingTime:mean" ,"aggr": ["none"]},
"ResponseTime": {"module": "**.sink", "scalar_name": "lifeTime:mean" ,"aggr": ["none"]}
```

Per raccogliere i dati esegui:
```sh
parse_data.py -c config.json -d database.db -j $(nproc) -r results/net-name_rho*.sca
```

Per analizzare i dati esegui:
```sh
analyze_data.py -c config.json -d database.db
```

## Visualizzazione dati
Puoi semplicemente aprire i file testuali prodotti (oppure aprirli con `gnumeric`).  
Per produrre grafici fai affidamento alle seguenti funzioni:
```python
#!/usr/bin/python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
import matplotlib as mpl
import matplotlib.colors as mc
#import pathlib

def set_fonts():
    """ 
    Set LaTeX-friendly fonts. Call this function at the beginning of your code
    """
    mpl.rcParams['font.family'] = 'Nimbus Sans'
    mpl.rcParams["figure.autolayout"] = True
    mpl.rc('text', usetex=True)
    mpl.rcParams.update({'font.size': 10})

def plot_line(ax, format, fname, label, xcol, ycol, errcol=None):
    """
    Plot a line from data
    
    Parameters
    ----------
    ax : 
        canvas for plotting. Refer to matplotlib.pyplot. Can ge the object returned by matplotlib.pyplot.subplots()
    format: str
        format string. Refer to matplotlib.pyplot
    fname: str or None
        name of a tab-separated column file. Column names are on the first row
    label: str
        label of the curve in the plot
    xcol:
        the x data for the plot 
        can be the name of a column in a dataframe if fname is a file with data
        can be a callable that is invoked on the dataframe
        can be a set list/array with data
    ycol:
        like xcol, but this is the y data of the plot
    errcol:
        like xcol but ti can aslo be none. If set it contains the error values to represent a confidence interval
    """
    if fname is not None:
        data = pd.read_csv(fname, sep='\t')
    use_data=fname is not None and not callable(xcol) and not callable(ycol) and not callable(errcol)
    xcol = xcol(data) if callable(xcol) else xcol
    ycol = ycol(data) if callable(ycol) else ycol
    errcol=errcol(data) if callable(errcol) else errcol
    data=data if use_data else None
    if errcol is not None:
        ax.errorbar(xcol, ycol, yerr=errcol, data=data, fmt=format, label=label, capsize=5)
    else:
        ax.plot(xcol, ycol, format, data=data, label=label)
```
Sample main for plot_line:
```python
fig, ax = plt.subplots()
ax.set(xlabel='$x$', ylabel='Time [s]')
plot_line(ax, 'o--', 'results/loadcurve.data', 'Response Time', '#f_l', 'ResponseTime', 'sigma(ResponseTime)')
pts=[x/10.0 for x in range(1, 10)]
plot_line(ax, '-', None, 'Theoretical Curve', pts, [theoretical(x) for x in pts])
plt.legend()
plt.savefig('sample.png')
plt.show()
```