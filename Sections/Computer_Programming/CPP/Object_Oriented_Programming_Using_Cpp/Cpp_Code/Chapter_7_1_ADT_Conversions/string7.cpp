/*********************************************************************

  Filename:  string7.cpp
  Chapter:   7      Ad Hoc Polymorphism
  Section:   7.1    ADT Conversions
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

// An implementation of dynamically allocated strings.
// with conversions and overloaded assignment

#include <iostream>
#include <string.h>
#include <assert.h>

using namespace std;

class my_string {
public:
   my_string() : len(0)
      { 
         s = new char[1];
         assert(s != 0); 
         s[0] = 0;
      }
   my_string(const my_string& str); //copy constructor
   my_string(const char* p);        //conversion constructor
   ~my_string() 
      { 
         delete []s; 
      }
   void print() const 
      { 
         cout << s << endl; 
      }
   // Had to make the parameter const so that the program can compile.  MK.   
   my_string operator=(const my_string& a);
   operator char*();     //conversion to char*
private:
   char*  s;
   int    len;
};

// No return type.  MK.
my_string::operator char*()
{
   char*  p = new char[len + 1];
   assert(p != 0);
   strcpy(p, s);
   return p;
}

my_string::my_string(const char* p)
{
   len = strlen(p);
   s = new char[len + 1];
   assert(s != 0);
   strcpy(s, p);
}

my_string::my_string(const my_string& str) : len(str.len)
{
   s = new char[len + 1];
   assert(s != 0);
   strcpy(s, str.s);
}

// Had to make the parameter const so that the program can compile.  MK.
my_string my_string::operator=(const my_string& a)
{
   if (this != &a) {       //a = a; do nothing
      if (a.len != len) {  //  if need different size string
         delete []s;
         len = a.len;
         s = new char[len + 1];
         assert(s != 0);
      }
      strcpy(s, a.s);
   }
   return *this;
}

int main()
{
   my_string s("Test it"), c("One"), d("Two");
   char* logo = "Geometrics Inc";
   char* logo2 = "MK Dynamics Inc";
   char* testit;

   testit = s;
   cout << testit << endl;     // check convert my_string to char*
   s = "One two three";
   s.print();
   s = logo;                   // check convert char* to my_string and =
   s.print();
   s = static_cast<my_string>(logo2);
   s.print();
   c = s = d;                  //check multiple assign on overloaded =
   c.print();
   s.print();
}
