/*********************************************************************

  Filename:  tracking.cpp
  Chapter:   6      Object Creation and Destruction
  Section:   6.11   No Constructor, Copy Constructor Other Mysteries
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

#include  <iostream>

using namespace std;

// personal data tracking

struct pers_data {
   int   age;           //in years
   int   weight;        //in kilograms
   int   height;        //in centimeters
   char  name[20];      //last name
};

void print(pers_data d)
{
   cout << d.name << " is " << d.age
        << " years old\n";
   cout << "weight : " << d.weight << "kg,  height : "
        << d.height << "cm." << endl;
}

int main()
{
   pers_data  laura = {3, 14, 88, "POHL"};
                  //construction off the stack

   print(laura);  //calls copy constructor
}
