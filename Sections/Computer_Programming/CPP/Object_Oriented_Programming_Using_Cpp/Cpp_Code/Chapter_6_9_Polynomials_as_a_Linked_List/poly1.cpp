/*********************************************************************

  Filename:  poly1.cpp
  Chapter:   6      Object Creation and Destruction
  Section:   6.9    Polynomial as a Linked List
  Compiler:  Borland C++     Version 5.0       Summer 1996
  Object Oriented Programming Using C++, Edition 2   By Ira Pohl

*********************************************************************/

//A polynomial represented as a singly linked list

#include <assert.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>

using namespace std;

//A polynomial represented as a singly linked list
struct term {
   int        exponent;
   double     coefficient;
   term*      next;
   term(int e, double c, term* n = 0)
       : exponent(e), coefficient(c), next(n) { }
   void print()
     {cout << coefficient << "x^" << exponent << " ";}
};

class polynomial {
public:
   polynomial(): h(0), degree(0) { }
   polynomial(const polynomial& p);
   polynomial(int size, double coef[], int expon[]);
   ~polynomial() { release(); }
   void print() const;
   void plus(polynomial a, polynomial b);
private:
   term*   h;
   int     degree;
   void    prepend(term*  t);   //add term to front
   void    add_term(term*& a, term*& b);
   void    release();           //garbage collect
   void    rest_of(term* rest); //add remaining terms
   void    reverse();           //reverse terms
};

void polynomial::reverse()       //in place
{
   term*  pred, *succ, *elem;

   if (h && (succ = h -> next)) {
      pred = 0;
      elem = h;
      while (succ) {
         elem -> next = pred;
         pred = elem;
         elem = succ;
         succ = succ -> next;
      }
      h = elem;
      h -> next = pred;
   }
}

void polynomial::release()
{
   term* temp = h;

   if (h) {  h = h -> next; delete temp; release(); }


}

inline void polynomial::prepend(term*t)
{
    t -> next = h;
     h = t;
}


void polynomial::print() const
{
   term* temp = h;

   if (h == 0) { cout << "0\n"; return; }
   while (temp){ temp -> print(); temp = temp -> next; }
   cout << endl;
}
//assumes ordering is correct expon[i] < expon[i+1]
polynomial::polynomial(int size, double coef[],
                       int expon[])
{
   term* temp = new term(expon[0], coef[0]);
   assert(temp != 0);

   h = 0;
   prepend(temp);               //create initial term
   for (int i = 1; i < size; ++i) {
       assert(expon[i - 1] < expon[i]);
       temp = new term(expon[i], coef[i]);
       assert(temp != 0);
       prepend(temp);          //add term
   }
   degree = h -> exponent;
}

polynomial::polynomial(const polynomial& p) :
                       degree(p.degree)
{
   term* elem = p.h, *temp;

   h = 0;
   while (elem) {              //term by term copying
      temp = new term(elem -> exponent,
                      elem -> coefficient);
      assert(temp != 0);
      prepend(temp);
      elem = elem -> next;
   }
   reverse();
}

void polynomial::add_term(term*& a, term*& b)
{
   term*  c;

   if (a -> exponent > b -> exponent) { //add a
      c = new term(a -> exponent, a -> coefficient) ;
      assert(c != 0);
      a = a -> next;
      prepend(c);
   }
   else if (a -> exponent < b -> exponent){ //add b
      c = new term(b -> exponent, b -> coefficient) ;
      assert(c != 0);
      b = b -> next;
      prepend(c);
   }
    else { //check on cancellation
       if (a -> coefficient + b -> coefficient != 0) {
           c = new term( a -> exponent,
                a -> coefficient + b -> coefficient);
           assert(c != 0);
           prepend(c);
        }
        a = a -> next;
        b = b -> next;
    }
}

void polynomial::rest_of(term* rest)
{
   term* temp;

   while (rest) {
      temp  = new term(rest -> exponent,
                       rest -> coefficient);
      assert(temp != 0);
      prepend(temp);
      rest = rest -> next;
   }
}

//c.plus(a,b) means c = a + b;
void polynomial::plus(polynomial a, polynomial b)
{
   term*    aterm = a.h, *bterm = b.h;

   release();  //garbage collect c, assumes not a or b
   h = 0;
   while (aterm && bterm)     //merge step
      add_term(aterm, bterm);
   if (aterm)
      rest_of(aterm);
   else if (bterm)
      rest_of(bterm);
   reverse();
   degree = ((h) ? h -> exponent: 0);
}

double coef[4] = {1, 2, 3, 4};
double coef2[4] = {-1,-2, -3, -4};
int    expo[4] = {0, 4, 14, 45};

main()
{
   polynomial p(4, coef2,expo), q(4,coef,expo), s;

   cout << "P(x) = ";
   p.print();
   cout << "Q(x) = ";
   q.print();
   s.plus(q,q);
   cout << "S(x) = Q(x) + Q(x) = ";
   s.print();
   s.plus(p, q);
   cout << "S(x) = P(x) + Q(x) = ";
   s.print();
}

