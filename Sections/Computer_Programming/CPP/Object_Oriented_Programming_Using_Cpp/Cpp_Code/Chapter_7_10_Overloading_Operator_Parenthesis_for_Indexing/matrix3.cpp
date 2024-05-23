/*********************************************************************

  Filename:  matrix3.cpp
  Chapter:   7      Ad Hoc Polymorphism
  Section:   7.10   Overloading () for Indexing
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//This is matrix not based on vect
//Shows () as index operator

#include  <iostream>          // Changed iostream.h to iostream
#include  <assert.h>

using namespace std;          // Added. MK.

class matrix {
public:
   matrix(int c, int r);
   ~matrix();
   double& operator()(int i, int j);
   double set_element(int i, int j, double d);
   matrix& operator=(const matrix& m);
   matrix& operator+=(matrix& m);
   void print() const;
private:
   int c_size, r_size;
   double  **p;
};

matrix:: matrix(int c, int r):c_size(c), r_size(r)
{
   p = new double*[c];
   assert(p != 0);

   for (int i = 0; i < c; ++i){
      p[i] = new double[r];
      assert(p[i] != 0);
   }
}

matrix:: ~matrix()
{
   for (int i = 0; i < c_size; ++i)
      delete [] p[i];
   delete [] p;
}

inline double& matrix::operator()(int i, int j)
{
   assert( i >= 0 && i < c_size && j >= 0 && j < r_size);
   return p[i][j];
}

matrix& matrix::operator=(const matrix& m)
{
   assert(m.c_size == c_size && m.r_size == r_size);
   int i, j;

   for (i = 0; i < c_size; ++i)
      for (j = 0; j < r_size; ++j)
         p[i][j] = m.p[i][j];
   return (*this);
}

matrix& matrix::operator+=(matrix& m)
{
   assert(m.c_size == c_size && m.r_size == r_size);
   int i, j;

   for (i = 0; i < c_size; ++i)
      for (j = 0; j < r_size; ++j)
         p[i][j] += m.p[i][j];
   return *this;
}

void matrix::print() const
{
   int i, j;
   for (i = 0; i < c_size; ++i) {
      cout << "\nrow  " << (i + 1) << endl;
      for (j = 0; j < r_size; ++j)
         cout << p[i][j] << "\t";
   }
   cout << endl;
}


void init_matrix(matrix& m, int c, int r, int start = 1)
{
   int i, j ;
   for (i = 0; i < c; ++i)
      for (j = 0; j < r; ++j)
         m(i, j) = start++;
}

int main()
{
   matrix m(3, 6) , n(3, 6);

   init_matrix(m, 3, 6, 1);
   init_matrix(n, 3, 6, 100);
   cout << "The matrix m contains ..." << endl;
   m.print();
   cout << endl;
   cout << "The matrix n contains ..." << endl;
   n.print();
   cout << endl;
   cout << "Performing n = n + m...." << endl;
   n += m;
   cout << endl;
   cout << "The matrix n contains ..." << endl;
   n.print();
}
