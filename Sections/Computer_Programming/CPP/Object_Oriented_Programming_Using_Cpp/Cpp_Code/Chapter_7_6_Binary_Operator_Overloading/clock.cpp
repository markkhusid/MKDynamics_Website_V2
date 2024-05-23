/*********************************************************************

  Filename:  clock.cpp
  Chapter:   7      Ad Hoc Polymorphism
  Section:   7.6    Unary, Binary Overloading
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//Clock to show overloading

#include <iostream>             // Changed iostream.h to iostream. MK.

using namespace std;            // Added. MK.

// I had to change "clock" to "myclock" because of interference
// with an object within iostream that is also declared as "clock"
class myclock {
public:
   myclock(unsigned long i);    //constructor and conversion
   void  print() const;         //formatted printout
   void  tick();                //add one second
   myclock operator++(){ tick(); return *this; }
   void reset (const myclock& c);
   friend myclock operator +(myclock c1, myclock c2);
   // I had to change operator - to a friend function
   // and update the parameter list to match operator +
   // otherwise the compiler complained about the number of 
   // arguments in the operation invocation.
   friend myclock operator -(myclock c1, myclock c2);
   friend myclock operator *(unsigned long m, myclock c);
   friend myclock operator *(myclock c, unsigned long m);
private:
   unsigned long  tot_secs, secs, mins, hours, days;
};

inline myclock::myclock(unsigned long i)
{
   tot_secs = i;
   secs = tot_secs % 60;
   mins = (tot_secs / 60) % 60;
   hours = (tot_secs / 3600) % 24;
   days = tot_secs / 86400;
}

void myclock::tick()
{
   myclock temp = myclock(++tot_secs);

   secs = temp.secs;
   mins = temp.mins;
   hours = temp.hours;
   days = temp.days;
}

void myclock::reset(const myclock& c)
{
   tot_secs = c.tot_secs;
   secs = c.secs;
   mins = c.mins;
   hours = c.hours;
   days = c.days;
}

myclock operator+(myclock c1, myclock c2)
{
   return (c1.tot_secs + c2.tot_secs);
}

myclock operator-(myclock c1, myclock c2)
{
   return (c1.tot_secs - c2.tot_secs);
}

myclock operator*(unsigned long m, myclock c)
{
   return (m * c.tot_secs);
}

myclock operator*(myclock c, unsigned long m)
{
   return (m * c.tot_secs);
}

void myclock::print() const
{
   cout << days << " d :" << hours << " h :"
        << mins << " m :" << secs << " s" << endl;
}

//Clock and overloaded operators

int main()
{
   myclock t1(59), t2(172799); //172799 = 2 days - 1 sec
   myclock t3(0);
   myclock c1(900), c2(400);

   cout << "initial times are" << endl;
   t1.print();
   t2.print();
   ++t1;  ++t2;
   cout << "after one second times are" << endl;
   t1.print();
   t2.print();
   cout << "\nt1 + t2   t1 * 5    6 * t1 * 5     6 * t1 * 5 - t2\n";
   t3 = t1 + t2;
   t3.print();
   t3 = t1 * 5;
   t3.print();
   t3 = 6 * t3;
   t3.print();
   t3 = t3 - t1;
   t3.print();
   c1.reset(c2);
   c2.reset(100);
   cout << "\nc1 and c2\n";
   c1.print();
   c2.print();
}

