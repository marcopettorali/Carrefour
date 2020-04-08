package carrefour;

//Decider implements the decision process of each customer when arrives in the market.
//Policy only affects the behavior of the module, not the structure.
simple Decider
{
    gates:
    	//customers come in from customer_in gate
        input customer_in;
        //when a customer leaves the market, a direct message is sent to the decider to let another enqueued customer to leave the queue
        input ack_in @directIn;
        //out is an array of gates, each one connected to a single till.
        output out[];
}
