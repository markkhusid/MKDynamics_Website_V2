// 02-constexpr.cpp : introducing the constexpr keyword
 
#include <print>
#include <cmath>
using namespace std;
 
// constexpr double PI1 = acos(-1.0);
constexpr double PI1 = 3.14159265358979323846; // Hardcoded value because compiler can not evaluate acos(-1.0) at compile time
constexpr double PI2 = 22.0 / 7.0;
 
static_assert(PI1 > 3.141 && PI1 < 3.143);
static_assert(PI2 > 3.141 && PI2 < 3.143);
 
int main() {
    println("PI1 = {}", PI1);
    println("PI2 = {}", PI2);
}