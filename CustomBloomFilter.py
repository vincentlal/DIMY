# Derived from https://github.com/dnanhkhoa/simple-bloom-filter/blob/master/bloomfilter/bloomfilter.py
# Modified version of python package simple-bloom-filter
# to give us access to the underlying bitarray and also 
# allow us to set filter size and number of hashes directly

#!/usr/bin/python
# -*- coding: utf-8 -*-
import mmh3
from bitarray import bitarray

class CustomBloomFilter():
    def __init__(self, filter_size, num_hashes):
        self.__size_used = 0

        self.__filter_size = filter_size
        self.__num_hashes = num_hashes

        self.__filter = bitarray(self.__filter_size, endian="little")
        self.__filter.setall(False)
    
    # def __repr__(self):
    #     return None
    
    @property
    def filter_size(self):
        return self.__filter_size

    @property
    def num_hashes(self):
        return self.__num_hashes

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
        if item not in self:
            for i in range(self.__num_hashes):
                self.__filter[mmh3.hash(item, i) % self.__filter_size] = True
            self.__size_used += 1

    def __contains__(self, item):
        for i in range(self.__num_hashes):
            if not self.__filter[mmh3.hash(item, i) % self.__filter_size]:
                return False
        return True
