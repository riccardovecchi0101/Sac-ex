import org.omnetpp.queueing.Queue; //server rete
import org.omnetpp.queueing.Sink; //rubinetto richieste
import org.omnetpp.queueing.Source; //sorgente messaggi (client)
import org.omnetpp.queueing.Router; //smista pacchetti

network rete // CHANGE_ME
{
    parameters:
        double mu = default(100);
        double rho ; // tasso di utilizzo = lambda/mu
        double lambda = rho*mu;
        double cv; //coefficiente di variazione
        src.interArrivalTime = 1.0s * exponential(1 / lambda);
        srv.serviceTime = 1.0s*lognormal(log(1.0/(mu*sqrt(1+cv^2))), sqrt(log(1+cv^2)));

    submodules:
        src: Source;
        srv: Queue;
        sink: Sink;

    connections:
        src.out --> srv.in++;
        srv.out --> sink.in++;
}