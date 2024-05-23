/*********************************************************************

  Filename:  ch_stac4.h
  Chapter:   6      Object Creation and Destruction
  Section:   6.2    Constructing a Dynamically Sized Stack
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//Stack implementation with constructor

#include <iostream>         // Changed iostream.h to iostream
#include <assert.h>
#include <cstring>         // Added for memcpy. MK

//ch_stack implementation with constructor.
class ch_stack {
public:
//the public interface for the ADT ch_stack
   explicit ch_stack(int size):
      max_len( size), top(EMPTY)
   { assert(size > 0);s = new char[size]; assert(s != 0);}
   ch_stack();
   ch_stack(const ch_stack& str);
   ch_stack(int size, const char str[]);
  ~ch_stack() { delete []s; }   //destructor
   void  reset() { top = EMPTY; }
   void  push(char c) { s[++top]= c; }
   char  pop() { return s[top--]; }
   char  top_of() const { return s[top]; }
   bool  empty() const { return (top == EMPTY); }
   bool  full() const { return (top == max_len - 1); }
private:
   enum  { EMPTY = -1 };
   char*  s;              //changed from s[max_len]
   int    max_len;
   int    top;
};

//default constructor for ch_stack
ch_stack::ch_stack():max_len(100),top(EMPTY)
{
   s = new char[100];
   assert(s != 0);
}

//domain transfer
ch_stack::ch_stack(int size, const char str[]):
   max_len(size)
{
   int i;
   assert(size > 0);
   s = new char[size];
   assert(s != 0);
   for (i = 0; i < max_len && str[i] != 0; ++i)
      s[i] = str[i];
   top = --i;
}

//Copy constructor for ch_stack of characters
ch_stack::ch_stack(const ch_stack& str):
   max_len(str.max_len),top(str.top)
{
   s = new char[str.max_len];
   assert(s != 0);
   memcpy(s, str.s, max_len);
}


