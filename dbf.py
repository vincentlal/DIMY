# Task 6 and 7
from CustomBloomFilter import CustomBloomFilter
from datetime import datetime, timedelta
import time
import threading
from QBF import QBF
from CBF import CBF
import http.client

class DBF():
    def __init__(self, startTime, endTime):
        self._startTime = startTime
        self._endTime = endTime
        self._dbf = CustomBloomFilter(filter_size=800000, num_hashes=2)
    
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
        self._dbf.add(encID)
    
    @property
    def filter(self):
        return self._dbf.filter

class DBFManager():
    # Constructor
    def __init__(self):
        # Create initial DBF objects
        self._dbfList = []
        self._processStarted = time.time()
        self._cycleRate = 600 # how many seconds 1 DBF is to be used for
        for i in range(0, 6):
            start = datetime.now() + timedelta(seconds=i*self._cycleRate)
            end = datetime.now() + timedelta(seconds=(i+1)*self._cycleRate)
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
        QBFJson = self.combineIntoQBF().jsonStringRepresentation()
        conn = http.client.HTTPConnection("ec2-3-26-37-172.ap-southeast-2.compute.amazonaws.com:9000")
        payload = str(QBFJson)
        headers = { 'Content-Type': "application/json" }
        conn.request("POST", "/comp4337/qbf/query", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    def uploadCBF(self):
        CBFJson = self.combineIntoCBF().jsonStringRepresentation()
        conn = http.client.HTTPConnection("ec2-3-26-37-172.ap-southeast-2.compute.amazonaws.com:9000")
        payload = str(CBFJson)
        headers = { 'Content-Type': "application/json" }
        conn.request("POST", "/comp4337/cbf/upload", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode('utf-8'))
        


    
    def __contains__(self, encID):
        for dbf in self._dbfList:
            if (encID in dbf):
                return True
        return False