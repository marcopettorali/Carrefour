#ifndef __CARREFOUR_GENERATOR_H_
#define __CARREFOUR_GENERATOR_H_

#include <omnetpp.h>
#include"Customer_m.h"
#include"Departure_m.h"

using namespace omnetpp;

class Generator : public cSimpleModule
{
  private:
    //these are the parameters to generate correct interarrival times and items in a cart values
    double meanInterArrivalTime_;
    double meanItemsInACart_;
    double normalMean_;
    double varianceOfItemsInACart_;

    //parameters to select the correct distributions
    int interArrivalDistribution_;
    int itemsInCartDistribution_;

    //self message for the timer
    cMessage* beep_;
  protected:
    //initialize the structures and the variables of this class and creates the first customer
    virtual void initialize();

    //handle beep_ message
    virtual void handleMessage(cMessage *msg);

    //destroy the messages at the end of the simulation
    ~Generator();
};

#endif
