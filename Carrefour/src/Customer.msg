//Customer message represents a customer coming into the supermarket
message Customer {
    //cartLenght represents the number of items in the cart.
    double cartLength;
    //arrivalTime contains the arrival time of the customer in the queue. 
    //This is needed to measure customer's waiting and response time.
    simtime_t arrivalTime;
}
