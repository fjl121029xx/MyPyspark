#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

# !/usr/bin/python
#
# Created by Albert Au Yeung (2010)
#
# An implementation of matrix factorization
#
try:
    import numpy
    from numpy import *
    from numpy import linalg as la
except:
    print("This implementation requires the numpy module.")
    exit(0)

###############################################################################

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
"""


def matrix_factorization(R,
                         P,
                         Q,
                         K,
                         steps=5000, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in range(steps):
        print('len(R)', len(R))
        for i in range(len(R)):
            print(i)
            print('len(R[i])', len(R[i]))
            for j in range(len(R[i])):
                print(j)
                print('R[i][j]', R[i][j])
                if R[i][j] > 0:
                    print('numpy.dot(P[i, :], Q[:, j])', numpy.dot(P[i, :], Q[:, j]))
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])
                    print('eij', eij)
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

        eR = numpy.dot(P, Q)
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
                    for k in range(K):
                        e = e + (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
        if e < 0.001:
            break
    return P, Q.T


###############################################################################

if __name__ == "__main__":
    R = [
        [5, 3, 0, 1],
        [4, 0, 0, 1],
        [1, 1, 0, 5],
        [1, 0, 0, 4],
        [0, 1, 5, 4],
    ]

    R = numpy.array(R)

    N = len(R)
    M = len(R[0])
    K = 2
    # print(N, M)
    P = numpy.random.rand(N, K)
    Q = numpy.random.rand(M, K)
    # print(P, Q)
    nP, nQ = matrix_factorization(R, P, Q, K)
    # print(nP, "-", nQ)

    print(mat(nP) * mat(nQ).T)
