/*********************************************************************

  Filename:  rational.cpp
  Chapter:   7      Ad Hoc Polymorphism
  Section:   7.3    Overloading and Function Selection
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//Overloading functions
#include  <iostream>       // Changed iostream.h to iostream.  MK.

using namespace std;       // Added. MK.

class rational{
public:
   rational(int n = 0) : a(n),q(1){}
   rational(int i, int j) : a(i), q(j){}
   rational(double r) : q(BIG), a(r * BIG){}
   void  print() const { cout << a << " / " << q ; }
   operator double(){return static_cast<double>(a)/q;}
   friend ostream& operator<<(ostream& out, rational x);
   friend istream& operator>>(istream& in, rational& x);
private:
   long  a, q;
   enum {BIG = 100};
};

ostream& operator<<(ostream& out, rational x)
{
    return (out << x.a << " / " << x.q << '\t');
}


istream& operator>>(istream& in, rational& x)
{
   return (in >> x.a >> x.q);
}

// Changed greater to is_greater since greater
// interferes with std::greater and compiler complains.
inline int      is_greater(int i, int j)
      { return ( i > j ? i : j); }
inline double   is_greater(double x, double y)
      { return ( x > y ? x : y); }
inline rational is_greater(rational w, rational z)
      { return ( w > z ? w : z); }

int main()
{
   int     i = 10, j = 5;
   float   x = 7.0;
   double  y = 14.5;
   rational w(10), z(3.5), zmax;

   cout << "\ngreater(" << i << ", " << j << ") = "
        << is_greater(i, j);
   cout << "\ngreater(" << x << ", " << y << ") = "
        << is_greater(x, y);
   cout << "\ngreater(" << i << ", " ;
   z.print();
   cout << ") = "
        << is_greater(static_cast<rational>(i), z);
   zmax = is_greater(w, z);
   cout << "\ngreater(";
   w.print();
   cout << ", ";
   z.print();
   cout << ") = ";
   zmax.print();
   // Commented code below.  MK.
   //cout << "\nEnter two longs for rational: ";
   cout << endl;
   cout << "Testing overloaded stream operation on rational class..." << endl;
   cin >> w;
   cout << w << endl;
}
