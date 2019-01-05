# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 11:14:52 2019

@author: NKrvavica
"""

import timeit
import numpy as np
import fqs


def numpy_roots(p):
    '''Finds roots of a polynomial by `numpy.roots`.'''
    roots = []
    for pi in p:
        roots.append(np.roots(pi))
    return roots


def eig_roots(p):
    '''Finds quartic roots via numerical eigenvalue solver
    `npumpy.linalg.eigvals` from a 4x4 companion matrix'''
    a, b, c, d = (p[:, 1]/p[:, 0], p[:, 2]/p[:, 0],
                  p[:, 3]/p[:, 0], p[:, 4]/p[:, 0])
    N = len(a)
    A = np.zeros((N, 4, 4))
    A[:, 1:, :3] = np.eye(3)
    A[:, :, 3] = - np.array([d, c, b, a]).T
    roots = np.linalg.eigvals(A)
    return roots


# --------------------------------------------------------------------------- #
# Tests
#
# Test speed of quartic solver compared to np.roots and np.linalg.eigvals
# --------------------------------------------------------------------------- #

# Number of samples (sets of randomly generated quartic coefficients)
N = 10000
range_coeff = 100
p = np.random.rand(N, 5)*(range_coeff) - range_coeff/2

start = timeit.default_timer()
roots1 = numpy_roots(p)
stop = timeit.default_timer()
time1 = stop - start
print('np.roots: {:.2f} ms'.format(time1*1000))

start = timeit.default_timer()
roots2 = eig_roots(p)
stop = timeit.default_timer()
time2 = stop - start
print('np.linalg.eigvals: {:.2f} ms'.format(time2*1000))
print('max err: ', (abs(np.sort(roots2, axis=1)
                    - (np.sort(roots1, axis=1)))).max())

start = timeit.default_timer()
roots3 = fqs.quartic_roots(p)
stop = timeit.default_timer()
time3 = stop - start
print('fqs.quartic_roots: {:.2f} ms'.format(time3*1000))
print('max err: ', (abs(np.sort(roots3, axis=1)
                    - (np.sort(roots1, axis=1)))).max())
# --------------------------------------------------------------------------- #