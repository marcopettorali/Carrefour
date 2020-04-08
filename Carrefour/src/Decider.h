#ifndef __CARREFOUR_DECIDER_H_
#define __CARREFOUR_DECIDER_H_

#include <omnetpp.h>
#include"Customer_m.h"
#include"Departure_m.h"


using namespace omnetpp;

class Decider : public cSimpleModule
{
  private:
    //the decider exploits the queue only if policy P1 is selected
    cQueue* queue_;

    //array of integers representing how many customers are there for each till
    //this structure is used to find the correct till towards the which we have to send an incoming customer
    //the way this structure is used depends on the policy
    int* tillCustomers_;

    //total number of tills in the supermarket
    int tillTotalNumber_;

    //decider module implements the policy, so it has to know which policy we want to apply
    int policy_;

    simsignal_t numCustomers_;

    //select the correct till according to the policy used (if there are any) and send there the customer
    void checkTillsAndPossiblySendCustomer(cMessage *msg = NULL);

    //customers arrivals must be handled differently in case of P1 or P2
    void handleMessageP1(cMessage *msg);
    void handleMessageP2(cMessage *msg);

  protected:

    //initialize the structures of this module
    virtual void initialize();

    //distinguish a P1 arrival from a P2 arrival
    virtual void handleMessage(cMessage *msg);

    //destroy the structures of this module
    ~Decider();
};

#endif
