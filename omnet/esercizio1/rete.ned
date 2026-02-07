import org.omnetpp.queueing.Queue; //server rete
import org.omnetpp.queueing.Sink; //rubinetto richieste
import org.omnetpp.queueing.Source; //sorgente messaggi (client)
import org.omnetpp.queueing.Router; //smista pacchetti

network rete // CHANGE_ME
{
    parameters:
        double lambda = default(10);
        double mu_l = default(10);
        double mu_c = default(10);
        double mu_r = default(1/0.07);
        double p = default(0.7);

        src.interArrivalTime = 1.0s * exponential(1 / lambda);
        router.randomGateIndex = uniform(0,1) <= p? 0: 1;  
        srv_l.serviceTime = 1.0s * exponential(1 / mu_l);
        srv_c.serviceTime = 1.0s * exponential(1 / mu_c);
        srv_r.serviceTime = 1.0s * exponential(1 / mu_r);

    submodules:
        router: Router;
        src: Source;
        srv_l: Queue;
        srv_c: Queue;
        srv_r: Queue;
        sink: Sink;

    connections:
        src.out --> router.in++;
        router.out++ --> srv_l.in++;
        router.out++ --> srv_r.in++;
        srv_r.out --> srv_c.in++;
        srv_l.out --> sink.in++;
        srv_c.out --> sink.in++;
}