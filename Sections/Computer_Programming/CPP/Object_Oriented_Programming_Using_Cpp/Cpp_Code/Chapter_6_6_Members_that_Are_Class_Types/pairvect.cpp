/*********************************************************************

  Filename:  pairvect.cpp
  Chapter:   6      Object Creation and Destruction
  Section:   6.5    A Class vect
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//test of safe array type vect

#include "vect1.h"

using namespace std;          // Added. MK.

class pair_vect {
public:
   pair_vect(int i) : a(i), b(i), size(i){ }
   int& first_element(int i);
   int& second_element(int i);
   int ub()const {return size -1;}
private:
   vect a, b;
   int size;
};

int& pair_vect::first_element(int i)
{   return a.element(i); }
int& pair_vect::second_element(int i)
{   return b.element(i);}

int main()
{
   int     i;
   pair_vect age_weight(5);  //age and weight

   cout << "table of age, weight\n";
   for (i = 0; i <= age_weight.ub(); ++i) {
      age_weight.first_element(i) = 21 + i;
      age_weight.second_element(i) = 135 + i;
      cout << age_weight.first_element(i) << ","         << age_weight.second_element(i)<< endl;
   }
}

