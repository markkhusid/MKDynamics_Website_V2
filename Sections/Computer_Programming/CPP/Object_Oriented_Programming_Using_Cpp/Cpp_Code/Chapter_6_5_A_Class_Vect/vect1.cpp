/*********************************************************************

  Filename:  vect1.cpp
  Chapter:   6      Object Creation and Destruction
  Section:   6.7    A Class vect
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//test of safe array type vect

#include "vect1.h"

using namespace std;    // Added. MK

int main()
{
   vect a(60), b[20];

   b[1].element(5) = 7;
   cout << b[1].element(5) << " 1 element 5\n";
   for (int i = 0; i <= a.ub(); ++i) {
      a.element(i) = i;
      cout << a.element(i) << "\t";
   }
   cout << endl;     // Added for output clarity
}
