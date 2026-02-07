[General]
ned-path = .;../environment/samples/queueinglib
network = rete 
cmdenv-config-name = rete_Base
qtenv-default-config = rete_Base

repeat = 5
sim-time-limit = 10000s
cpu-time-limit = 60s
**.vector-recording = false

[Config rete_Base]
description = "Global scenario"
**.sink_global.lifeTime.result-recording-modes = +histogram
%for p in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.4, 0.45, 0.5]:

[Config rete_p${"%03d" % int(p*100)}]
extends = rete_Base
**.p = ${p}
%endfor