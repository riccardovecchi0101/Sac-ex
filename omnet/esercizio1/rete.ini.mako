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
**.sink.lifeTime.result-recording-modes = +histogram
%for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:

[Config rete_p${"%02d" % int(p*10)}]
extends = rete_Base
**.p = ${p}
%endfor