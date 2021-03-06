# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 03:47:14 2021

@author: kazuk
"""

MIN_BUCKET = 0
MAX_BUCKET = 15

def bucket_sort(aList):
    buckets = list()
    for i in range(MIN_BUCKET, MAX_BUCKET + 1):
        buckets.append(None)

    for i in aList:
        buckets[aList[i]] = aList[i]

    x = 0
    for i in range(MIN_BUCKET, MAX_BUCKET + 1):
        if buckets[i] is not None:
            aList[x] = buckets[i]
            x += 1

    return aList
