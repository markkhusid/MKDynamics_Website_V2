/*********************************************************************

  Filename:  vect1.h
  Chapter:   6      Object Creation and Destruction
  Section:   6.5    A class vect
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//Implementation of a safe array type vect

#include  <iostream>    // changed iostream.h to iostream. MK
#include  <assert.h>

//Implementation of a safe array type vect
class vect {
public:
   explicit vect(int n = 10);
   ~vect() { delete []p; }
   int&  element(int i);                 //access p[i]
   int  ub() const {return (size - 1);}  //upper bound
private:
   int*  p;
   int   size;
};

vect::vect(int n) : size(n)
{
   assert(n > 0);
   p = new int[size];
   assert(p != 0);
}

int& vect::element(int i)
{
   assert (i >= 0 && i < size);
   return p[i];
}
