from QBF import QBF
import json
import base64

class CBF(QBF):
    def __init__(self, DBFList):
        super().__init__(DBFList)

    # Override
    def printState(self):
        print(f'Combined into single CBF with state: {self._QBF.getIndexes()}')

    # Override
    def rawJSON(self):
        return {"CBF" : base64.b64encode(self._QBF.filter).decode('utf-8')}

    # Override
    def jsonStringRepresentation(self):
        return json.dumps({"CBF" : base64.b64encode(self._QBF.filter).decode('utf-8')}, indent=4)

