from CustomBloomFilter import CustomBloomFilter

class QBF():
    def __init__(self, DBFList):
        self._QBF = CustomBloomFilter(size=800000, fp_prob=0.0000062)
        combinedBitArray = DBFList[0].filter
        for i in range(1, 6):
            combinedBitArray |= DBFList[i].filter
        self._QBF.filter = combinedBitArray
    
    def __repr__(self):
        return str(self._QBF.filter)
    
    def __contains__(self, encID):
        return encID in self._QBF
