# Task 6 and 7
# pip3 install simplebloomfilter
from bloomfilter import BloomFilter
from ecdh import generateECDHObjects, verifyEphID, calcEncID
from datetime import datetime, timedelta
import time
import threading
import sys

class DBF():
    def __init__(self, startTime, endTime):
        self._startTime = startTime
        self._endTime = endTime
        self._dbf = BloomFilter(size=800000, fp_prob=0.0000062)
    
    def __contains__(self, encID):
        return encID in self._dbf
    
    def __repr__(self):
        return f'DBF(startTime:{self._startTime}, endTime:{self._endTime}'

    def getStartTime(self):
        return self._startTime
    
    def getEndTime(self):
        return self._endTime
    
    def add(self, encID):
        self._dbf.add(encID)

class DBFManager():
    # Constructor
    def __init__(self):
        # Create initial DBF objects
        self._dbfList = []
        self._processStarted = time.time()
        self._terminated = False
        self._cycleRate = 600 # how many seconds 1 DBF is to be used for
        for i in range(0, 6):
            start = datetime.now() + timedelta(seconds=i*self._cycleRate)
            end = datetime.now() + timedelta(seconds=(i+1)*self._cycleRate)
            dbfObj = DBF(start, end)
            self._dbfList.append(dbfObj)
        # Cycle DBFs every 10 minutes with no drift
        self._dbfThread = threading.Thread(target=self.initialiseDBFCycling, name='DBF-Cycler', daemon=True)
        self._dbfThread.start()
        
    def terminate(self):
        self._terminated = True
    
    def initialiseDBFCycling(self):
        while True:
            time.sleep(self._cycleRate - ((time.time() - self._processStarted) % float(self._cycleRate)))
            print("tick")
            self.cycleDBFs()
           
    def __repr__(self):
        return str(self._dbfList)
    
    def cycleDBFs(self):
        start = self._dbfList[-1].getEndTime()
        end = start + timedelta(seconds=self._cycleRate)
        self._dbfList.pop(0)
        self._dbfList.append(DBF(start,end))
        print(self)

    # Add EncID to DBF
    def addToDBF(self, encID):
        self._dbfList[-1].add(encID) # add to current DBF
    
    def __contains__(self, encID):
        for dbf in self._dbfList:
            if (encID in dbf):
                return True
        return False