# Sinusoidal, amplitude, phase and frequency estimation
# author: allee updated by sdm

import numpy as np                     # need math and arrays
from numpy.linalg import inv           # matrix inversion
import matplotlib.pyplot as plt        # and plotting

# First, let's create a noisy set of "samples" of a cosine wave...
A = 1                  # the Amplitude
ftrue = 0.1            # true frequency
phi = np.pi/4          # phase shift
N = 20                 # number of samples
var = 10/16            # modify the noise
mu = 0                 # additional noise

n = np.arange(0,N,1)                        # sample points 0 <= n < N
s = np.cos((2 * np.pi * ftrue * n) + phi)   # an array of cos values
wgn = np.sqrt(var) * np.random.randn(N) + mu  # an array of noise
x = A*s + wgn                               # mult by amplitude and add noise
plt.scatter(n,x,label='samples')            # plot the noisy samples
plt.xlabel('sample')
plt.ylabel('value')
plt.title('actual and sampled values')
plt.plot(n,s,label="actual signal")         # plot the clean samples

f0 = np.arange(0.01,0.5,0.01)               # array of frequencies

# Remember that matrix products are done right to left!
# And each entry in J is:
# J = Xt * H * inv( Ht * H ) * Ht * X
# where X is the sample array and Xt its transpose
# H is the array of sine and cos entries for a particular frequency
# inv() is the inverse of the contents
# and * is the dot product

J = []                                      # maximize J to find f 
h = np.zeros((N,2))                         # create the H matrix
for f in f0:                                # for every frequency to try...
    h[:,0] = np.cos(2 * np.pi * f * n)      # column 0 gets the cosines
    h[:,1] = np.sin(2 * np.pi * f * n)      # column 1 gets the sines
    a = np.dot(h.transpose(),x)             # Ht * X
    b = inv(np.dot(h.transpose(),h))        # inverse of the product Ht * H
    c = np.dot(b,a)                         # dot the above two terms
    d = np.dot(h,c)                         # and with H
    J.append(np.dot(x.transpose(),d))       # and with Xt and into the list

print(J)
indexmax = np.argmax(J)                     # find the index of largest value
f_est = f0[indexmax]                        # then get the corresponding freq
print('freq est', f_est, '\tvs actual', ftrue)

h[:,0] = np.cos(2 * np.pi * f_est * n)      # set up H with that frequency
h[:,1] = np.sin(2 * np.pi * f_est * n)

# apply least squares estimator
# [alpha1 alpha2] = inv(Ht * H) * Ht * X

a = np.dot(h.transpose(),x)             # Ht * X
b = inv(np.dot(h.transpose(),h))        # inverse of Ht * H
c = np.dot(b,a)                         # product of the above

a_est = np.linalg.norm(c)               # amplitude = sqrt(alpha1^2 + alpha2^2)
print('a_est', a_est, '\tvs actual',A )

phase_est = np.arctan(-c[1]/c[0])       # compute the estimated phase
print('phase_est', phase_est, '\tvs actual', phi)

# now use all the above to plot the estimated curve
s_est =  a_est * np.cos((2 * np.pi * f_est * n) + phase_est)
plt.plot(n, s_est, label="estimated signal")
plt.legend()
plt.show()
