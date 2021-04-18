from CustomBloomFilter import CustomBloomFilter
import base64
import json
class QBF():
    def __init__(self, DBFList):
        self._QBF = CustomBloomFilter(filter_size=800000, num_hashes=3)
        dbfStrInfo = [x.state() for x in DBFList]
        dbfStrInfoJoined = '[ ' + ', '.join(dbfStrInfo) + ' ]'
        print(f'Currently have {len(DBFList)} DBFs with states: {dbfStrInfoJoined}')
        combinedBitArray = DBFList[0].filter
        for i in range(1, len(DBFList)):
            combinedBitArray |= DBFList[i].filter
        self._QBF.filter = combinedBitArray
        print(f'Combined into single QBF with state: {self._QBF.getIndexes()}')
    
    def __repr__(self):
        return str(self._QBF.filter)
    
    def __contains__(self, encID):
        return encID in self._QBF
    
    def base64Representation(self):
        return base64.b64encode(self._QBF.filter)
    
    def rawJSON(self):
        return {"QBF" : base64.b64encode(self._QBF.filter).decode('utf-8')}

    def jsonStringRepresentation(self):
        return json.dumps({"QBF" : base64.b64encode(self._QBF.filter).decode('utf-8')}, indent=4)