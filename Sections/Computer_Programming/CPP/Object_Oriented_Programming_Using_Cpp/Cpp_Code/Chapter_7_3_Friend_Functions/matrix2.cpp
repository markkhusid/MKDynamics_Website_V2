/*********************************************************************

  Filename:  matrix2.cpp
  Chapter:   7      Ad Hoc Polymorphism
  Section:   7.3    Friend Functions
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

class matrix;                 // forward reference

#include  <iostream>        // Changed iostream.h to iostream. MK.
#include  <assert.h>
#include  "vect2.h"

using namespace std;          // Added. MK.

class matrix {
public:
   matrix(int d1, int d2);
   ~matrix();
   int  ub1() const { return(s1 - 1); }
   int  ub2() const { return(s2 - 1); }
   void print() const;
   int&  element(int i, int j);
private:
   int**  p;
   int    s1, s2;
   friend    vect mpy(const vect& v, const matrix& m);
};

matrix::matrix(int d1, int d2) : s1(d1), s2(d2)
{
   assert (d1 > 0 && d2 > 0);
   p = new int*[s1];
   assert(p != 0);
   for (int i = 0; i < s1; ++i)
      p[i] = new int[s2];
}

matrix::~matrix()
{
   for (int i = 0; i <= ub1(); ++i)
      delete p[i];
   delete []p;
}

int& matrix::element(int i, int j)
{
   assert(i >= 0 || i <= ub1() || j >= 0 || j <= ub2());
   return p[i][j];
}


vect mpy(const vect& v, const matrix& m)
{
   assert(v.size == m.s1);    //check sizes
   //use privileged access to p in both classes
   vect  ans(m.s2);
   int   i, j;

   for (i = 0; i <= m.ub2(); ++i) {
      ans.p[i] = 0;
      for (j = 0; j <= m.ub1(); ++j)
         ans.p[i] += v.p[j] * m.p[j][i];
   }
   return ans;
}

void matrix::print() const
{
   int j;
   for (int i = 0; i <= ub1(); ++i) {
      cout << "\nrow  " << (i + 1) << endl;
      for (j = 0; j <= ub2(); ++j)
         cout << p[i][j] << "\t";
   }
   cout << endl;
}


void init_vect(vect& v, int start, int incr)
{
   for (int i = 0; i <= v.ub(); ++i) {
      v[i] = start;
      start += incr;
   }
}

int main()
{
   vect   a(3), b(3), c(6), d(6);
   matrix m(3, 6) ;
   int    i, j;

   a[0] = 1 + (a[1] = 1 + ( a[2] = 1)) ;
   init_vect(b, 1, 1);
   init_vect(c, 10, 10);
   init_vect(d, 100, 1);

   cout << "vector a is\n";
   a.print();
   cout << "\nvector b is\n";
   b.print();
   cout << "\nvector c is\n";
   c.print();
   cout << "\nvector d is\n";
   d.print();

   for (i = 0; i <= m.ub1(); ++i)
      for (j = 0; j <= m.ub2(); ++j)
         m.element(i, j) = i + j;

   cout << "\nmatrix m is\n";
   m.print();

   c = mpy(a, m);
   cout << "\nvector c product is\n";
   c.print();
}
