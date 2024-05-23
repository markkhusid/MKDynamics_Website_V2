// Overloading the operator +
#include <iostream>
#include <string>
#include <cstring>

using namespace std;

class my_string {
    public:
        my_string() { 
            len = 0; s = new char[1]; 
        }

        explicit my_string(int n) {
            s = new char[n+1];
            len = n;
        }

        void assign(const char* str)
        {
            delete []s;
            len = strlen(str);
            s = new char[len + 1];
            strcpy(s, str);
        }

        int length() const {
            return len;
        }

        void print() const {
            cout << s << "\nLength: " << len << endl;
        }

        my_string& operator = (const my_string& a);

        friend my_string& operator+ (const my_string& a, const my_string& b);
    
    private:
        char* s;
        int len;
};

// Overload +
my_string& operator+(const my_string& a, const my_string& b)
{
    my_string* temp = new my_string(a.len + b.len);

    strcpy(temp->s, a.s);
    strcat(temp->s, b.s);
    return *temp;
}

void print(const char* c) // file scope print
{
    cout << c << "\nLength: " << strlen(c) << endl;
}

int main()
{
    my_string one, two, both;
    char three[40] = {"My name is Charles Babbage."};

    one.assign("My name is Alan Turing.");
    two.assign(three);
    print(three);   // file scope print called

    if (one.length() <= two.length())
        one.print();
    else
        two.print();
    both = one + two;   // plus overloaded as concatenate
    both.print();
}