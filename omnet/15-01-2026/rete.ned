import org.omnetpp.queueing.Queue; //server rete
import org.omnetpp.queueing.Sink; //rubinetto richieste
import org.omnetpp.queueing.Source; //sorgente messaggi (client)
import org.omnetpp.queueing.Router; //smista pacchetti
import org.omnetpp.queueing.Clone;

network rete // CHANGE_ME
{
    parameters:
        double lambda = default(40);
        double mu_1 = default(25);
        double mu_2 = default(40);

        double p = default(0.5);

        src.interArrivalTime = 1.0s * exponential(1 / lambda);
        router.randomGateIndex = uniform(0,1) <= p? 0: 1;  
        srv_1.serviceTime = 1.0s * exponential(1 / mu_1);
        srv_clone_1.serviceTime = 1.0s *0;
        srv_clone_2.serviceTime = 1.0s *0;
        srv_2.serviceTime = 1.0s * exponential(1 / mu_2);


    submodules:
        router: Router;
        src: Source;
        srv_1: Queue;
        srv_2: Queue;
        srv_clone_1: Clone;
        srv_clone_2: Clone;
        sink_1: Sink;
        sink_2: Sink;
        sink_global: Sink;

    connections:
        src.out --> router.in++;
        router.out++ --> srv_1.in++;
        router.out++ --> srv_2.in++;
        srv_1.out --> srv_clone_1.in++;
        srv_2.out --> srv_clone_2.in++;
        srv_clone_1.out++  --> sink_1.in++;
        srv_clone_1.out++ --> sink_global.in++;
        srv_clone_2.out++ --> sink_2.in++;
        srv_clone_2.out++ --> sink_global.in++;

}   