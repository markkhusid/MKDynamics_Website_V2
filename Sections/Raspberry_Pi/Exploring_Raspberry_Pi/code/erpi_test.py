#!/usr/bin/python
# A Python program that calls C program code
import erpi
import numpy

print "Start of the Python program"
print erpi.hello("World")

val = erpi.integrate_sin(0, numpy.pi, 1000000)
print "The integral of sin(x) from 0 to Pi is: ", val
print "End of the Python program"
