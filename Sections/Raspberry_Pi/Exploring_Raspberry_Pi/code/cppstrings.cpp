#include <iostream>
#include <sstream>                  // to tokenize the string
//#include <cstring>                // how to include the C++ equivalent of a C header

using namespace std;

int main() {
    string a = "hello ";
    char temp[] = {'w', 'o', 'r', 'l', 'd', '!', '\0'};
    string b(temp);
    
    a[0] = 'H';
    string c = a + b;
    cout << "The string c is: " << c << endl;
    cout << "The length of c is: " << c.length() << endl;
    
    int loc = c.find_first_of('w');
    c.replace(loc, 1, 1, 'W');
    cout << "The string c is now: " << c << endl;
    
    if (string("cat") < string("dog")) {
        cout << "cat comes before dog (lexiographically)\n";
    }
    
    c.insert(5, " to the");
    cout << "The c string is now: " << c << endl;
    
    // tokenize string using spaces - could use Boost.Tokenizer
    // or C++11 to improve syntax.  Using stringstream this time.
    stringstream ss;
    ss << c;                        // put the string c into the stringstream
    string token;
    while (getline(ss, token, ' ')) {
        cout << "Token: " << token << endl;
    }
    
    return 0;
}

