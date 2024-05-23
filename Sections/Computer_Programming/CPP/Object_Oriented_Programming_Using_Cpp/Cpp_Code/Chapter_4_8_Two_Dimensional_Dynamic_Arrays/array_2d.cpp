// Dynamic arrays in two dimensions
#include <iostream>
using namespace std;

struct twod {
    double **   base;
    int         row_size, column_size;
};

void allocate (int r, int s, twod & m)
{
    m.base = new double * [s];
    for (int i = 0; i < s; ++i)
        m.base[i] = new double[r];
    m.row_size = r;
    m.column_size = s;
}

void deallocate(twod & m)
{
    for (int i = 0; i < m.column_size; ++i)
        delete [] m.base[i];
    delete [] m.base;
    m.row_size = 0;
    m.column_size = 0;
}

double find_max(const twod & m)
{
    int i, j;
    double max = m.base[0][0];

    for (i = 0; i < m.column_size; ++i)
        for (j = 0; j < m.row_size; ++j)
            if (m.base[i][j] > max)
                max = m.base[i][j];
    return (max);
}

int main ()
{
    twod    a, b;
    int     i, j;

    allocate(2, 3, a);
    allocate(4, 6, b);

    for (i = 0; i < a.column_size; ++i)
        for (j = 0; j < b.row_size; ++j)
            a.base[i][j] = i * j;
    
    for (i = 0; i < b.column_size; ++i)
        for (j = 0; j < b.row_size; ++j)
            b.base[i][j] = i * j;

    cout << find_max(a) << " max in size 2 * 3\n";
    cout << find_max(b) << " max in size 4 * 6\n";
}