/*********************************************************************

  Filename:  matrix1.cpp
  Chapter:   6      Object Creation and Destruction
  Section:   6.8    Two Dimensional Arrays
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

// Adapted by Mark Khusid
//A two-dimensional safe array type matrix

#include  <iostream>       // Changed iostream.h to iostream.  MK.
#include  <assert.h>

using namespace std;       // Added. MK.

//A two-dimensional safe array type matrix
class matrix {
public:
   matrix(int d1, int d2);
   ~matrix();
   int  ub1() const { return(s1 - 1); }
   int  ub2() const { return(s2 - 1); }
   int&  element(int i, int j);
private:
   int**  p;
   int    s1, s2;
};
 matrix::matrix(int d1, int d2) : s1(d1), s2(d2)
{
   cout << "\nActivated Constructor..." << endl;      // Added instrumentation. MK.
   assert(d1 > 0 && d2 > 0);
   p = new int*[s1];
   assert(p != 0);
   for (int i = 0; i < s1; ++i){
      p[i] = new int[s2];
      assert(p[i] != 0);
   }
}
matrix::~matrix()
{
   cout << "\nActivated Destructor..." << endl;       // Added instrumentation. MK.
   for (int i = 0; i <= ub1(); ++i)
      delete p[i];
   delete []p;
}

int& matrix::element(int i, int j)
{
   assert(i >= 0 || i <= ub1() || j >= 0 || j <= ub2());
   return p[i][j];
}

int main()
{
   matrix a(4, 4), b(4, 6);      // Removed extra variable c (not used). MK.
   int i, j;

   cout << "\nThe matrix a contains: " << endl; // Added. MK.
   for (i = 0; i <= a.ub1(); ++i) {
      cout << "\n";
      for (j = 0; j <= a.ub2(); ++j) {
         a.element(i, j) = i + j;
         cout << a.element(i, j) << "\t";
      }
   }
   
   cout << "\n" << endl;   // Added. MK.

   cout << "\nThe matrix b contains: " << endl; // Added. MK.
   for (i = 0; i <= b.ub1(); ++i) {
      cout << "\n";
      for (j = 0; j <= b.ub2(); ++j) {
         b.element(i, j) = i + j;
         cout << b.element(i, j) << "\t";
      }
   }

   cout << "\n" << endl;   // Added. MK.

}
