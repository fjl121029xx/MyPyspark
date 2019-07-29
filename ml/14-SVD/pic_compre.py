#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'fjl'

import pandas as pd
import numpy
import tensorflow as tf
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
from sklearn import datasets
from skimage import io


def getImgAsMat(index):
    ds = datasets.fetch_olivetti_faces()
    return np.mat(ds.images[index])


def getImgAsMatFromFile(filename):
    img = io.imread(filename, as_grey=True)
    return np.mat(img)


def plotImg(imgMat):
    plt.imshow(imgMat, cmap=plt.cm.gray)
    plt.show()


def recoverBySVD(imgMat, k):
    # singular value decomposition
    U, s, V = la.svd(imgMat)
    # choose top k important singular values (or eigens)
    Uk = U[:, 0:k]
    Sk = np.diag(s[0:k])
    Vk = V[0:k, :]
    # recover the image
    imgMat_new = Uk * Sk * Vk
    return imgMat_new


# -------------------- main --------------------- #
A = getImgAsMatFromFile('pic.jpg')
plotImg(A)
A_new = recoverBySVD(A, 15)
plotImg(A_new)