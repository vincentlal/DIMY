# Task 6 and 7
from CustomBloomFilter import CustomBloomFilter
from datetime import datetime, timedelta
import time
import threading
from QBF import QBF
from CBF import CBF
import requests

class DBF():
    def __init__(self, startTime, endTime):
        self._startTime = startTime
        self._endTime = endTime
        self._dbf = CustomBloomFilter(filter_size=800000, num_hashes=3)
    
    def __contains__(self, encID):
        return encID in self._dbf
    
    def __repr__(self):
        return f'DBF(startTime:{self._startTime}, endTime:{self._endTime}'

    @property
    def startTime(self):
        return self._startTime

    @property
    def endTime(self):
        return self._endTime
    
    def add(self, encID):
        indexes = self._dbf.add(encID)
        print(indexes)

    @property
    def filter(self):
        return self._dbf.filter

class DBFManager():
    # Constructor
    def __init__(self):
        # Create initial DBF object
        self._dbfList = []
        self._processStarted = time.time()
        self._cycleRate = 600 # how many seconds 1 DBF is to be used for
        start = datetime.now()
        end = datetime.now() + timedelta(seconds=self._cycleRate)
        dbfObj = DBF(start, end)
        self._dbfList.append(dbfObj)
        # Cycle DBFs every 10 minutes with no drift
        self._dbfThread = threading.Thread(target=self.initialiseDBFCycling, name='DBF-Cycler', daemon=True)
        self._dbfThread.start()

    def initialiseDBFCycling(self):
        while True:
            time.sleep(self._cycleRate - ((time.time() - self._processStarted) % float(self._cycleRate)))
            self.cycleDBFs()

    def __repr__(self):
        return str(self._dbfList)

    def cycleDBFs(self):
        start = self._dbfList[-1].endTime
        end = start + timedelta(seconds=self._cycleRate)
        if (len(self._dbfList) == 6):
            self._dbfList.pop(0)
        self._dbfList.append(DBF(start,end))
        print(self)

    # Add EncID to DBF
    def addToDBF(self, encID):
        self._dbfList[-1].add(encID) # add encID to current DBF

    def combineIntoQBF(self):
        return QBF(self._dbfList)

    def combineIntoCBF(self):
        return CBF(self._dbfList)

    def sendQBFToEC2Backend(self):
        url = "http://ec2-3-26-37-172.ap-southeast-2.compute.amazonaws.com:9000/comp4337/qbf/query"
        payload = self.combineIntoQBF().rawJSON()
        headers = {"Content-Type": "application/json"}
        res = requests.request("POST", url, json=payload, headers=headers)
        resJSON = res.json()
        if (resJSON['result'] == "No Match"):
            print("QBF Uploaded to EC2 Server - No Match - You are safe.")
        else:
            print("QBF Uploaded to EC2 Server - Match - You are potentially at risk. Please consult a health official, self-isolate and do a COVID-19 test at your earliest convenience.")

    def uploadCBF(self):
        url = "http://ec2-3-26-37-172.ap-southeast-2.compute.amazonaws.com:9000/comp4337/cbf/upload"
        payload = self.combineIntoCBF().rawJSON()
        headers = {"Content-Type": "application/json"}
        res = requests.request("POST", url, json=payload, headers=headers)
        resJSON = res.json()
        print(resJSON)
        if (resJSON['result'] == "Success"):
            print("CBF successfully uploaded to EC2 Server")
        else:
            print("Failed to upload CBF - rejected by EC2 Server")

    def __contains__(self, encID):
        for dbf in self._dbfList:
            if (encID in dbf):
                return True
        return False