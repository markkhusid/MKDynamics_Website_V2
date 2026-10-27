#include <string>
#include <boost/python.hpp>					// .hpp convention for c++ headers
using namespace std;						// just like cpp for source files

namespace exploringpi {						// keep the global namespace clean
	
	string hello(string name) {				// returns Hello <name entered> !
		return ("Hello " + name + "!");
	}
	
	double integrate_sin(double a, double b, int n) {		// integral of sine over interval
		double sum = 0, dx = (b-a)/n;
		for (int i = 0; i < n; i++) {
			sum += sin((a+i)*dx);
		}
		return sum*dx;
	}
}

BOOST_PYTHON_MODULE(erpi) {					// the module is called erpi
	using namespace boost::python;			// require the boost.python namespace
	using namespace exploringpi;			// bring in our custom namespace
	def ("hello", hello);					// make hello() visible to python
	def ("integrate_sin", integrate_sin);	// make integrate_sin() visible to python
}


	
	
