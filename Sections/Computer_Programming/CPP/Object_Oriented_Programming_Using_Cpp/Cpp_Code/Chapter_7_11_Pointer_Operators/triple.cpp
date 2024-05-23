/*********************************************************************

  Filename:  triple.cpp
  Chapter:   7      Ad Hoc Polymorphism
  Section:   7.11   Pointer Operators
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

// This file was not present together with the downloadable files that 
// accompany Ira Pohl's book.  This file was typed and adapted from 
// Ira Pohl's book.

#include <iostream>

using namespace std;

class triple {
public:
    triple(int a, int b, int c) {
        i = a;
        j = b;
        k = c;
    }

    void print() {
        cout << "\ni = " << i << ", j = "
             << j << ", k = " << k;
    }

private:
    int i, j, k;
};

triple unauthor(0, 0, 0);

class t_ptr {
public:
    t_ptr(bool f, triple* p) {
        access = f;
        ptr = p;
    }

    triple* operator ->() ;

private:
    bool    access;
    triple* ptr;
};

triple* t_ptr::operator->()
{
    if (access) {
        cout << "\nauthorized access";
        return (ptr);
    }
        
    else {
        cout << "\nunauthorized access";
        return &unauthor;
    }
}

int main()
{
    triple a(1, 2, 3), b(4, 5, 6);
    t_ptr ta(false, &a), tb(true, &b);

    cout << "Attempting to print triple a...";
    ta -> print();

    cout << endl; cout << endl;

    cout << "Attempting to print triple b...";
    tb -> print();
}
