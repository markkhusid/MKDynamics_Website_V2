/*********************************************************************

  Filename:  ch_stac4.cpp
  Chapter:   6      Object Creation and Destruction
  Section:   6.2    Constructing a Dynamically Sized Stack
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//Stack implementation with constructor

#include <iostream>        // Changed iostream.h to iostream. MK
#include "ch_stac4.h"


using namespace std;       // Added. MK

int cnt_char(char c, ch_stack s)
{
   int  count = 0;

   while (!s.empty())
      count += (c == s.pop());
   return count;
}

int main()
{
   ch_stack  typea(100);    //size only
   ch_stack  typeb;         //no size
   ch_stack  typec(50, "My name is Ira Pohl!\n");  //size and initializer
   ch_stack  typed(typec);
   char reverseline[200];
   char a [30] = {"My name is Laura Pohl!\n"};
   char b [40] = {"My name is Debra Dolsberry!\n"};
   int  i = 0;

   cout << "\nNumber of a's in typec shoud be 2. It is "
        << cnt_char('a', typec) << endl;

   typea.reset();

   while (a[i])
      if (!typea.full())
    typea.push(a[i++]);

   i = 0;
   while (!typea.empty())
      reverseline[i++] = typea.pop();
   reverseline[i] = '\0';
   cout << reverseline;

   i = 0;
   while (b[i])
      if (!typeb.full())
    typeb.push(b[i++]);

   i = 0;
   while (!typeb.empty())
      reverseline[i++] = typeb.pop();
   reverseline[i] = '\0';
   cout << reverseline;

   i = 0;
   while (!typec.empty())
      reverseline[i++] = typec.pop();
   reverseline[i] = '\0';
   cout << reverseline;
   i = 0;

   while (!typed.empty())
      reverseline[i++] = typed.pop();
   reverseline[i] = '\0';
   cout << reverseline;
}
