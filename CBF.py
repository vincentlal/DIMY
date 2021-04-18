from QBF import QBF
import json
import base64

class CBF(QBF):
    def __init__(self, DBFList):
        super().__init__(DBFList)

    def jsonStringRepresentation(self):
        return json.dumps({"CBF" : base64.b64encode(self._QBF.filter).decode('utf-8')}, indent=4)

