#include <iostream>
#include <assert.h>
using namespace std;

double avg_arr(const int a[], int size)
{
    int sum = 0;
    for (int i = 0; i < size; ++i)
        sum += a[i];
    return static_cast<double>(sum) / size;
}

int main()
{
    int *   data;
    int     size;

    for (int n_loop = 0; n_loop < 1; ++n_loop) {
        cout << "\nEnter array size: ";
        cin >> size;
        assert(size > 0);

        data = new int[size];
        assert (data != 0);

        for (int j = 0; j < size; ++j) {
            cout << "\nEnter data at position " << j << " -> ";
            cin >> data[j];
        }
        
        cout << " average is " << avg_arr(data, size) << endl;
        delete [] data;
    }
}