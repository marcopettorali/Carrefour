#include "Generator.h"
#include <cmath>

Define_Module(Generator);

void Generator::initialize(){
    //read the distribution of items in a cart and interarrival times
    interArrivalDistribution_ = getParentModule()->par("interArrivalDistribution");
    itemsInCartDistribution_ = getParentModule()->par("itemsInCartDistribution");

    //read the mean values of items in a cart and interarrival times (also variance for items in a cart used into lognormal)
    meanInterArrivalTime_ = getParentModule()->par("meanInterArrivalTime");
    meanItemsInACart_ = getParentModule()->par("meanItemsInACart");

    //pick the variance for the itemsInCart property of a Customer message (only for norm and lognorm)
    if(itemsInCartDistribution_ == 1){
        varianceOfItemsInACart_ = getParentModule()->par("varianceOfItemsInACart");
    }
    else if(itemsInCartDistribution_ == 2){
        varianceOfItemsInACart_ = getParentModule()->par("varianceOfItemsInACart");
        //to avoid the possibility of having negative values in a normal distribution
        if(meanItemsInACart_ < (sqrt(varianceOfItemsInACart_) * 7)) {
            varianceOfItemsInACart_ = meanItemsInACart_/7;
            varianceOfItemsInACart_ *= varianceOfItemsInACart_;
        }
    }

    //since OmNET++'s lognormal() wants the mean of the associated normal distribution,
    //we have to feed it not the lognormal mean value, but the normal's one instead
    normalMean_ =  log(meanItemsInACart_) - varianceOfItemsInACart_/2;

    //create the feedback message
    beep_ = new cMessage("beep");

    //first customer comes as soon as the simulation starts
    scheduleAt(simTime(), beep_);

}

//handle beep_ message; each time a beep_ arrives, a new customer is generated
void Generator::handleMessage(cMessage *msg){
    Customer* cust = new Customer("newCustomer");
    cust->setArrivalTime(simTime());
    switch(itemsInCartDistribution_){ //switch is better so that we can implement additional distributions
        case 0 :
            //exponential distribution
            //NOTE: Using RNG #1 to generate the flow of service times
            cust->setCartLength(exponential(meanItemsInACart_, 1));
            break;
        case 1 :
            //lognormal distribution
            //NOTE: Using RNG #1 to generate the flow of service times
            cust->setCartLength(lognormal(normalMean_,varianceOfItemsInACart_, 1));
            EV<<"The cartLenght is -> "<<cust->getCartLength();
            break;
        case 2 :
            //normal distribution
            //NOTE: Using RNG #1 to generate the flow of service times
            cust->setCartLength(normal(meanItemsInACart_,varianceOfItemsInACart_, 1));
            EV<<"The cartLenght is -> "<<cust->getCartLength();
            break;
        default :
            EV << "This type of distribution for items in a cart is not supported yet!";

    }

    //throw this customer to the tills
    send(cust, "out");

    //wait some time before generating next customer
    if(interArrivalDistribution_ == 0){
        //exponential distribution
        //NOTE: Using RNG #0 to generate the flow of arrivals
        scheduleAt(simTime()+exponential(meanInterArrivalTime_, 0), beep_);
    }else{
        EV << "This type of distribution for interarrival times is not supported yet!";
    }
}

Generator::~Generator(){
    //delete beep_ message
    cancelAndDelete(beep_);
}
