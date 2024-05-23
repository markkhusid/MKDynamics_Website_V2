// Miles are converted to kilometers
#include <iostream>

const double m_to_k = 1.609;    // Conversion constant

inline double mi_to_km(int miles)
{
    return (miles * m_to_k);
}

int main()
{
    int miles;
    double kilometers;

    do {
        std::cout << "\nEnter distance in miles: ";
        std::cin >> miles;

        kilometers = mi_to_km(miles);
        std::cout << "\nThis is approximately " << static_cast<int>(kilometers) 
            << "km." << std::endl;
    } while (miles > 0);
}
