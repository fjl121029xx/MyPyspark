#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wsc'

"""
    特征性选择
        过滤式：方差
        
    主成分分析PCA
    
"""
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
import pandas as pd


def var():
    """
    特征选择：删除低方差特征
    :return:
    """

    vr = VarianceThreshold(threshold=1.0)
    data = vr.fit_transform([[0, 2, 0, 3],
                             [0, 1, 4, 3],
                             [0, 1, 1, 3]])
    print(data)
    return None


def pca():
    """
    PCA
    :return:
    """
    pca = PCA(n_components=0.9)
    data = pca.fit_transform([[2, 8, 4, 5],
                              [6, 3, 0, 8],
                              [5, 4, 9, 1]])
    print(data)
    return None


def instacard():
    """
    kaggle市场篮子分析
    D:/work/all/aisles.csv                  商品所属具体物品类别
    D:/work/all/departments.csv
    D:/work/all/order_products__prior.csv   订单与商品信息
    D:/work/all/order_products__train.csv
    D:/work/all/orders.csv                  用户订单信息
    D:/work/all/products.csv                商品信息
    D:/work/all/sample_submission.csv
    :return:
    """

    prior = pd.read_csv('D:/work/all/order_products__prior.csv')
    products = pd.read_csv('D:/work/all/products.csv')
    orders = pd.read_csv('D:/work/all/orders.csv')
    aisles = pd.read_csv('D:/work/all/aisles.csv ')

    # 合并表   用户-物品类别
    _mg = pd.merge(prior, products, on=['product_id', 'product_id'])
    _mg = pd.merge(_mg, orders, on=['order_id', 'order_id'])
    mt = pd.merge(_mg, aisles, on=['aisle_id', 'aisle_id'])

    mt.head(10)
    # 交叉表  分组
    cross = pd.crosstab(mt['user_id'], mt['aisle'])
    cross.head(10)
    # 主成分分析
    pca = PCA(n_components=0.9)
    data = pca.fit_transform(cross)
    print(data)
    return None


if __name__ == '__main__':
    instacard()
