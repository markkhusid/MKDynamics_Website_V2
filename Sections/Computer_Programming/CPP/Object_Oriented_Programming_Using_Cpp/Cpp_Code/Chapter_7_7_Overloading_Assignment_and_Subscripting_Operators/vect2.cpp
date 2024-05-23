/*********************************************************************

  Filename:  vect1.cpp
  Chapter:   6      Object Creation and Destruction
  Section:   6.7    A Class vect
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//test of safe array type vect

#include "vect2.h"

using namespace std;    // Added. MK

int main()
{
   const int ARR_SIZE = 20;
   vect a(10), b(5), c, d(20), e_from_arr(ARR_SIZE);
   int arr[ARR_SIZE];
   int i;

   cout << "The upper bound of vector a is : " << a.ub() << endl;

   cout << "The upper bound of vector b is : " << b.ub() << endl;

   cout << endl;

   cout << "Initialize vect a...." << endl;
   for (i = 0; i <= a.ub(); ++i)
      a[i] = i;
     
   cout << "The vector a contains : ";
   a.print();

   cout << "The vector b contains : ";
   b.print();

   cout << endl;

   cout << "Perform b = a (vect to vect assignment)..." << endl;
   b = a;

   cout << "The vector b contains : ";
   b.print();

   cout << endl;

   // Default constructor
   cout << "The vector c contains : ";
   c.print();

   cout << "Perform c = b (vect to vect assignment)..." << endl;
   c = b;

   cout << endl;

   cout << "The vector d contains : ";
   d.print();

   cout << "Perform d = a + c (vect to vect addition)..." << endl;
   cout << "The vector a contains : ";
   a.print();
   cout << "The vector c contains : ";
   c.print();
   d = a + c;

   cout << "The vector d contains : ";
   d.print();

   cout << endl;

   cout << "The vector e_from_arr contains : ";
   e_from_arr.print();

   cout << "Initialize array arr..." << endl;
   for (i = 0; i < ARR_SIZE; ++i) {
      arr[i] = i + 10;
   }

   cout << "Array arr contains : " << endl;
   for (i = 0; i < ARR_SIZE; ++i) {
      cout << arr[i] << " ";
   }
   cout << endl;

   cout << "Convert array arr into vect e_from_arr..." << endl;
   e_from_arr = vect(arr, ARR_SIZE);

   cout << "The vector e_from_arr contains : ";
   e_from_arr.print();
}
