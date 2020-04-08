package carrefour.simulations;
import carrefour.*;

network Carrefour
{
    parameters:
        //the number of tills contained in the supermarket
        int tillsNumber;

        //avg speed of humans' walk is 1 m/s
        //avg interdistance between tills is 2 m.
        double delta @unit(s) = default(2s);

        //policy = 1 -> single queue, multiple servers
        //policy = 2 -> multiple queues, one for each server
        int policy;

        //this parameter represents the capacity of tills in the supermarket.
        //this value is expressed in number of processable items per second
        double capacity = default(0.3);
        
        //this parameter represents the mean interarrival time of the customers
        double meanInterArrivalTime @unit(s);
        
        //this parameter represents the mean number of items in a cart
        double meanItemsInACart;
        
        //this parameter represents the variance of items in a cart (used for lognormal distribution)
        double varianceOfItemsInACart = default(0); //If it's used it will be changed in .ini file so never =0 (default)
        
        //0: exponential distribution of interarrival times
        int interArrivalDistribution;
        
        //0: exponential distribution of the number of items in a cart
        //1: lognormal distribution of the number of items in a cart
        int itemsInCartDistribution;
        
       
        @signal[waitTime] (type=simtime_t);
        @statistic[stats_waitTime] (source="waitTime"; record=vector;);
        @signal[responseTime] (type=simtime_t);
        @statistic[stats_responseTime] (source="responseTime"; record=vector;);
        @signal[numCustomers] (type=long);
        @statistic[stats_numCustomers] (source="numCustomers"; record=timeavg;);
      
        
    submodules:
        generator: Generator;
        decider: Decider;
        tills[tillsNumber]: Till{
            parameters:
                position = index;
        }
    connections:
        generator.out --> decider.customer_in;
        
        //connecting each output of the decider with each till only if policy == 1
        for j=0..(sizeof(tills)-1) {
            decider.out++ --> {  delay = delta*j*(2 - policy); } --> tills[j].in;
        }
}
