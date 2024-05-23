/*********************************************************************

  Filename:  modulo.cpp
  Chapter:   6      Object Creation and Destruction
  Section:   6.1    Classes with Constructors
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//Modulo numbers and constructor initialization

#include  <iostream>

using namespace std;

const int  modulus = 60;

// Modulo numbers and constructor initialization
class  mod_int {
public:
   mod_int(int i);     //constructor declaration
   void  assign(int i) { v = i % modulus; }
   void  print() const { cout << v << '\t'; }
   const static int modulus = 60;
private:
   int  v;
};

inline  mod_int::mod_int(int i = 0)
{
    v = i % modulus;
}
const int  mod_int::modulus;

int main()
{
   int      seconds = 400;
   mod_int  z(seconds);

   cout << seconds << " seconds equals "
        << seconds / 60 << " minutes ";
   z.print();
   cout << " seconds" << endl;
}


