#include <iostream>
using namespace std;

typedef int (*CallbackType)(int);           // used to tidy up syntax

int squareCallback(int x){                  // callback function that squares
    return x*x;
}

int cubeCallback(int x){                    // callback function that cubes
    return x*x*x;
}

int doMath(int num, CallbackType callback){
    return callback(num);                   // call the function that is passed
}

int main(){
    cout << "Math program -- the value of 5: " << endl;
    cout << "-> squared is: " << doMath(5, &squareCallback) << endl;
    cout << "-> cubed is: " << doMath(5, &cubeCallback) << endl;
    return 0;
}
