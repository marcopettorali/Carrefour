#ifndef __CARREFOUR_TILL_H_
#define __CARREFOUR_TILL_H_

#include <omnetpp.h>
#include"Customer_m.h"
#include"Departure_m.h"

using namespace std;
using namespace omnetpp;

class Till : public cSimpleModule
{
  private:
    //queue_ represents the queue of a single till
    cQueue* queue_;

    //processing_ contains the currently served customer
    Customer* processing_;

    //beep_ message for the timer that simulates the service time
    cMessage* beep_;

    //position_ represents the position of this till in the array of tills
    int position_;

    //capacity_ represents the speed at which this till serves one unit of cart length
    double capacity_;

    //serveCustomer() is called when a new customer reaches the head of line of the queue
    void serveCustomer(Customer* msg);

    //serveNextCustomer() is called to make the queue advance when a customer leaves the till
    void serveNextCustomer();

    //attributes for statistics
    simsignal_t responseTime_;
    simsignal_t waitTime_;

  protected:
    //it initializes the main structures of this module
    virtual void initialize();

    //handleMessage() recognizes if a beep or a customer message is received
    virtual void handleMessage(cMessage *msg);

    //when the service time for a customer expires, beep_ is received by the till
    void handleBeep(cMessage* msg);

    //when a customer reaches the till, he's handled according to the policy
    void handleCustomer(Customer* msg);

    //it destroys the structures
    ~Till();
};

#endif
