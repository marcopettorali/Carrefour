#include "Till.h"
#include <cstring>

Define_Module(Till);

//it initializes the main structures of this module
void Till::initialize()
{
    //let's initialize the beep_ message, the queue and the currently served customer to null
    this->beep_ = new cMessage("beep");
    this->queue_ = new cQueue("line");
    this->processing_ = NULL;

    //the parent network is required to set the 'capacity' parameter
    this->capacity_= getParentModule()->par("capacity");
    this->position_ = par("position");

    //let's get the signals to make statistics about the response and the waiting time of the customers
    responseTime_ = registerSignal("responseTime");
    waitTime_ = registerSignal("waitTime");

    }

//handleMessage() recognizes if a beep or a customer message is received
void Till::handleMessage(cMessage *msg){
    if(msg->isSelfMessage())
        handleBeep(msg);
    else {
        handleCustomer(check_and_cast<Customer*>(msg));
    }
    //nothing else to do: these are the only two cases of message

}

//when a customer reaches the till, he's handled according to the policy
void Till::handleCustomer(Customer *msg) {

    //if the till is empty the customer gets served
    if(this->processing_ == NULL && this->queue_->isEmpty()) {
        serveCustomer(msg);
    }

    //otherwise it gets enqueued
    else {
        this->queue_->insert(msg);
    }
}

//when the service time for a customer expires, beep_ is received by the till
void Till::handleBeep(cMessage *msg){
    emit(responseTime_, simTime() - processing_->getArrivalTime());

    //we prepare and send a message back to the decider to let it know that a customer has left
    Departure *dep = new Departure("departure");
    dep->setTillPosition(position_);
    //Note: the parent network is required to call the Decider instance "decider"
    cModule *targetModule = getParentModule()->getSubmodule("decider");
    this->sendDirect(dep, targetModule, "ack_in");
    //we serve next customer (if there are any)
    serveNextCustomer();
}

//serveCustomer() is called when a new customer reaches the head of line of the queue
void Till::serveCustomer(Customer *msg) {
    emit(waitTime_, simTime() - msg->getArrivalTime());
    //we set a timer representing the service time of this customer, calculated as cartLength/capacity;
    double procTime = msg->getCartLength()/this->capacity_;
    this->processing_ = msg;
    this->scheduleAt(simTime() + procTime, this->beep_);
}

//serveNextCustomer() is called to make the queue advance when a customer leaves the till
void Till::serveNextCustomer() {
    //we pick old customer to destroy it later
    Customer* old = this->processing_;

    //if there is another enqueued customer, serve it
    if(!this->queue_->isEmpty()) {
        Customer* nextProc = check_and_cast<Customer*>(this->queue_->pop());
        serveCustomer(nextProc);
    }
    //otherwise just stay idle
    else {
        this->processing_ = NULL;
    }

    //let's destroy the old and useless customer leaving
    delete old;
}

//let's destroy the structures built for this module
Till::~Till() {
    //let's destroy the beep_message
    cancelAndDelete(this->beep_);

    //let's destroy the elements left in the queue
    while(!this->queue_->isEmpty()) {
        Customer* tmp = check_and_cast<Customer*>(this->queue_->pop());
        delete tmp;
    }
    delete this->queue_;

    //destroy the current served customer
    if(processing_) {
        delete processing_;
    }
}
