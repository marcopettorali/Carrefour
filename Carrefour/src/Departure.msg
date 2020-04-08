//Departure message is returned to the decider when a customer leaves
message Departure {
    //tillPosition represents the position of the till that served the customer.
    //This is needed to help the decider to know which till is the less crowded
    int tillPosition;
}
