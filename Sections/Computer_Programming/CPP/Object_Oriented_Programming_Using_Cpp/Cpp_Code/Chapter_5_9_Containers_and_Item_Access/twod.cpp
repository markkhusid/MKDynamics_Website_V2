// Dynamic arrays in two dimensions
#include <iostream>
using namespace std;

class twod {
public:
    bool    allocate(int r, int s);    // pseudo - constructor
    
    void    deallocate();              // pseudo - destructor
    
    double& element_lval(int i, int j) const
        { return base[i][j]; }
    
    double  element_rval(int i, int j) const
        { return base[i][j]; }
    
    int     r_size() const { return row_size;    }
    int     c_size() const { return column_size; }

private:
    double**    base;
    int         row_size, column_size;
};

bool twod::allocate(int r, int s)
{
    base = new double*[s];
    if (base == 0)  // allocation failed
        return false;
    for (int i = 0; i < s; ++i) {
        base[i] = new double[r];
        if (base[i] == 0)   // allocation failed
            return false;
    }
    row_size = r;
    column_size = s;
    return true;
}

void twod::deallocate()
{
    for (int i = 0; i < column_size; ++i)
        delete [] base[i];
    delete [] base;
    row_size = 0;
    column_size = 0;
}

double find_max(const twod& m)
{
    int i, j;
    double max = m.element_rval(0,0);

    for (i = 0; i < m.c_size(); ++i)
        for (j = 0; j < m.r_size(); ++j)
            if (m.element_rval(i, j) > max)
                max = m.element_rval(i, j);
    return max;
}

void print_2d(twod& m)
{
    int i, j;

    for (i = 0; i < m.c_size(); ++i) {
        for (j = 0; j < m.r_size(); ++j)
            cout << m.element_rval(i, j) << " ";
        cout << "\n";
    }
}

int main ()
{
    twod    a, b;
    int     i, j;

    a.allocate(2, 3);
    b.allocate(4, 6);

    for (i = 0; i < a.c_size(); ++i)
        for (j = 0; j < b.r_size(); ++j)
            a.element_lval(i, j) = i * j;
    
    for (i = 0; i < b.c_size(); ++i)
        for (j = 0; j < b.r_size(); ++j)
            b.element_lval(i, j) = i * j;

    cout << "\n\nPrinting 3x2 matrix A...\n";
    print_2d(a);
    cout << "\n\nPrinting 6x4 matrix B...\n";
    print_2d(b);
    cout << "\nMax element in size 3x2 matrix A is -> " << find_max(a) << endl;
    cout << "\nMax element in size 6x3 matrix B is -> " << find_max(b) << endl;
}