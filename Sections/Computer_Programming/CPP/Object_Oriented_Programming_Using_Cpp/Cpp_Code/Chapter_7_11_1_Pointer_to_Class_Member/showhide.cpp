/*********************************************************************

  Filename:  showhide.cpp
  Chapter:   7      Ad Hoc Polymorphism
  Section:   7.11   Pointer Operators
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//Pointer to class member.

#include <iostream>           // Changed iostream.h to iostream. MK.

using namespace std;          // Added. MK.

class X {
public:
   int  visible;
   void print()
      { cout << "\nhide = " << hide
             << " visible = " << visible; }
   void reset() { visible = hide; }
   void set(int i) { hide = i; }
private:
   int  hide;
};

typedef void (X::*pfcn)();

int main()
{
   X  a, b, *pb = &b;
   int X::*pXint = &X::visible;
   pfcn pF = &X::print;

   a.set(8); a.reset();
   b.set(4); b.reset();
   a.print();
   a.*pXint += 1;
   a.print();
   cout << "\nb.visible = " << pb ->*pXint;
   (b.*pF)();
   pF = &X::reset;
   (a.*pF)();
   a.print();
   cout << endl;
}