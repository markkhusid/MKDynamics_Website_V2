/*********************************************************************

  Filename:  vect2.h
  Chapter:   7      Ad Hoc Polymorphism
  Section:   7.7    Friend Functions
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

class matrix;                 // forward reference

#include  <iostream>         // Changed iostream.h to iostream. MK.
#include  <assert.h>

using namespace std;          // Added. MK.

class vect {
public:
   vect() { size = 10; p = new int[size]; }
   explicit vect(int n);
   vect(const vect& v);
   vect(const int a[], int n);  //initialize by array
   ~vect() { delete []p; }
   int  ub() const { return (size - 1); }  //upper bound
   vect& operator=(const vect& v);  //overload assignment
   void print() const;
   int&  operator[](int i) ;         //range checked
   vect operator+(const vect& v);
private:
   int*  p;
   int   size;
   friend vect mpy(const vect& v, const matrix& m);
};

vect::vect(int n) : size(n)
{
   assert(n > 0);
   p = new int[size];
   assert(p != 0);
}

vect::vect(const int a[], int n) : size(n)
{
   assert(n > 0);
   p = new int[size];
   assert(p != 0);
   for (int i = 0; i < size; ++i)
      p[i] = a[i];
}

vect::vect(const vect& v) : size(v.size)
{
   p = new int[size];
   assert(p != 0);
   for (int i = 0; i < size; ++i)
      p[i] = v.p[i];
}

int& vect::operator[](int i)
{
   assert(i >= 0 && i < size);
   return p[i];
}

vect& vect::operator=(const vect& v)
{
   int s = (size < v.size) ? size : v.size;

   if (v.size != size)
      cerr << "copying different size arrays "
           << size << " and " << v.size << endl;
   for (int i = 0; i < s; ++i)
      p[i] = v.p[i];
   return (*this);
}


void vect::print() const
{
   for (int i = 0; i <= (size-1); ++i)
      cout << p[i] << "\t";
   cout << endl;
}

vect vect::operator+(const vect& v)
{
   assert(size == v.size);
   vect  sum(size);
   for (int i = 0; i < size; ++i)
      sum.p[i] = p[i] + v.p[i];
   return sum;
}


