# Derived from https://github.com/dnanhkhoa/simple-bloom-filter/blob/master/bloomfilter/bloomfilter.py
# Modified version of python package simple-bloom-filter to give us access to the underlying bitarray

#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import mmh3

from bitarray import bitarray

class CustomBloomFilter():
    def __init__(self, size, fp_prob=1e-6):
        self.__size_used = 0
        self.__size = size
        self.__fp_prob = fp_prob

        if self.__size:
            self.__filter_size = math.ceil(
                -self.__size * math.log(self.__fp_prob) / math.log(2) ** 2
            )
            self.__num_hashes = round(self.__filter_size * math.log(2) / self.__size)

            self.__filter = bitarray(self.__filter_size, endian="little")
            self.__filter.setall(False)
        else:
            self.__filter = bitarray(endian="little")
    
    @property
    def filter_size(self):
        return self.__filter_size

    @property
    def num_hashes(self):
        return self.__num_hashes

    @property
    def fp_prob(self):
        return self.__fp_prob

    @property
    def size(self):
        return self.__size

    @property
    def filter(self):
        return self.__filter

    @filter.setter
    def filter(self, new_filter):
        self.__filter = new_filter

    def __len__(self):
        return self.__size_used

    def add(self, item):
        if item not in self and self.__size_used < self.__size:
            for i in range(self.__num_hashes):
                self.__filter[mmh3.hash(item, i) % self.__filter_size] = True
            self.__size_used += 1

    def __contains__(self, item):
        for i in range(self.__num_hashes):
            if not self.__filter[mmh3.hash(item, i) % self.__filter_size]:
                return False
        return True
