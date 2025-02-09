//
// Generated file, do not edit! Created by nedtool 5.5 from Departure.msg.
//

#ifndef __DEPARTURE_M_H
#define __DEPARTURE_M_H

#if defined(__clang__)
#  pragma clang diagnostic ignored "-Wreserved-id-macro"
#endif
#include <omnetpp.h>

// nedtool version check
#define MSGC_VERSION 0x0505
#if (MSGC_VERSION!=OMNETPP_VERSION)
#    error Version mismatch! Probably this file was generated by an earlier version of nedtool: 'make clean' should help.
#endif



/**
 * Class generated from <tt>Departure.msg:1</tt> by nedtool.
 * <pre>
 * message Departure
 * {
 *     int tillPosition;
 * }
 * </pre>
 */
class Departure : public ::omnetpp::cMessage
{
  protected:
    int tillPosition;

  private:
    void copy(const Departure& other);

  protected:
    // protected and unimplemented operator==(), to prevent accidental usage
    bool operator==(const Departure&);

  public:
    Departure(const char *name=nullptr, short kind=0);
    Departure(const Departure& other);
    virtual ~Departure();
    Departure& operator=(const Departure& other);
    virtual Departure *dup() const override {return new Departure(*this);}
    virtual void parsimPack(omnetpp::cCommBuffer *b) const override;
    virtual void parsimUnpack(omnetpp::cCommBuffer *b) override;

    // field getter/setter methods
    virtual int getTillPosition() const;
    virtual void setTillPosition(int tillPosition);
};

inline void doParsimPacking(omnetpp::cCommBuffer *b, const Departure& obj) {obj.parsimPack(b);}
inline void doParsimUnpacking(omnetpp::cCommBuffer *b, Departure& obj) {obj.parsimUnpack(b);}


#endif // ifndef __DEPARTURE_M_H

