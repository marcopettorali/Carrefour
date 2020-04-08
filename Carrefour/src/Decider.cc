#include "Decider.h"
#include <cstring>

Define_Module(Decider);

//initialize the structures of this module
void Decider::initialize()
{
    //the parent network is required to set policy and tillTotalNumber parameters
    policy_= getParentModule()->par("policy");
    tillTotalNumber_= getParentModule()->par("tillsNumber");

    //create an array representing how many customers are present for each till and inizialize it to 0
    tillCustomers_= new int [tillTotalNumber_];
    memset(tillCustomers_, 0x00, tillTotalNumber_*sizeof(int));

    numCustomers_ = registerSignal("numCustomers");

    //if policy is P1, queue is useful; P2 doesn't need any queue in the decider
    if(policy_==1)
        this->queue_ = new cQueue("line");
}

//distinguish P1 and P2 policies
void Decider::handleMessage(cMessage *msg)
{
    //N is the number of customers in the market
    int N = 0;
    switch ( policy_ )
          {
             case 1://P1
                handleMessageP1(msg);
                //get N from the dimension of the decider's queue
                N = queue_->getLength();
                break;
             case 2://P2
                 handleMessageP2(msg);
                break;
             default:
                EV<<"Error! We need to abort the simulation!";
          }


    for(int i = 0; i < tillTotalNumber_; ++i)
        //add to N the number of customers in every till
        N += tillCustomers_[i];

    emit(numCustomers_, N);
}

//handle a P1 arrival
void Decider::handleMessageP1(cMessage *msg){

    //a customer has reached the tills' zone of the supermarket
    if(strcmp(msg->getName(),"newCustomer") == 0)
        //if the queue is not empty, all the tills are busy: enqueue the customer
        if(!queue_->isEmpty())
            queue_->insert(msg);
        //else check if we can send this customer directly to the tills
        //queue can be empty but all the tills can be busy
        else{
            checkTillsAndPossiblySendCustomer(msg);
        }

    //it's a departure message reached from a till after a departure of a customer
    else {
        Departure *dep = check_and_cast<Departure*>(msg);
        //update the number of customers in that till
        tillCustomers_[dep->getTillPosition()]--;
        //if there is at least one person in the queue, send the customer to the tills
        //note that at least the till that released the customer is idle
        if(!queue_->isEmpty())
            checkTillsAndPossiblySendCustomer();
        delete dep;
    }

}

//find a free till
void Decider::checkTillsAndPossiblySendCustomer(cMessage *msg){
    //msg is null when the new customer is the head of line of the queue
    //msg is not null when the next customer to be processed must be taken from the queue
    if(!msg)
        msg = check_and_cast<cMessage*>(queue_->pop());

    //let's choose the index of the till to which send the customer
    int destTill;

    //check all the tills and stop at the first empty till
    for(destTill = 0;destTill < tillTotalNumber_; destTill++){
        if(tillCustomers_[destTill] > 0)
            continue;
        else
            break;
    }

    //if no empty till was found, we are in the case of empty queue a customer arrives
    //otherwise at least one till is surely empty; we are certain to never reinsert a message in the queue
    if(destTill == tillTotalNumber_)
        queue_->insert(msg);
    //else send the customer to the found till and increment its counter of customers
    else{
        tillCustomers_[destTill]++;
        //Delta*j will be considered as part of the service time because the till is already busy during the traversing of the customer
        send(msg, "out",destTill);
    }
}


//handle a P2 arrival
void Decider::handleMessageP2(cMessage *msg){
    //if a new customer arrives
    if(strcmp(msg->getName(),"newCustomer") == 0){

        //we choose the less crowded till
        int destTill=0;
        for(int i=0; i<tillTotalNumber_ ; i++)
            if(tillCustomers_[i] < tillCustomers_[destTill])
                destTill = i;

        //we send the customer to the less crowded till and increment its counter of customers
        tillCustomers_[destTill]++;
        send(msg, "out",destTill);
    }

    else {
        //It's a departure message from a till
        Departure *dep = check_and_cast<Departure*>(msg);

        //update the amount of customers in that till
        tillCustomers_[dep->getTillPosition()]--;
        delete dep;
    }
}

Decider::~Decider() {

    delete[] tillCustomers_;

    //if policy is P2 we have only to delete the array with the counters for each till
    if(policy_==2)
        return;

    //delete the queue only if used (in P1 policy)
    while(!queue_->isEmpty()) {
        Customer* tmp = check_and_cast<Customer*>(this->queue_->pop());
        delete tmp;
    }
    delete this->queue_;
}
