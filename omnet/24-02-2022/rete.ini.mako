[General]
ned-path = .;../environment/samples/queueinglib
network = rete
sim-time-limit = 300s
repeat = 3
**.vector-recording = false

[Config rete_Base]
description = "MG1 – sweep rho e cv"
**.mu = 100
**.sink.lifeTime.result-recording-modes = +histogram
**.srv.serviceTime.result-recording-modes = +histogram


% for rho in [0.7, 0.9]:
%   for cv in [0.5,1.0,1.5]:

[Config rete_rho${int(rho*100)}_cv${int(cv*10)}]
extends = rete_Base
**.rho = ${rho}
**.cv = ${cv}

%   endfor
% endfor
