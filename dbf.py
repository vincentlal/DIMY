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

    def state(self):
        return self._dbf.getIndexes()

    @property
    def startTime(self):
        return self._startTime

    @property
    def endTime(self):
        return self._endTime
    
    def add(self, encID):
        indexes = self._dbf.add(encID)
        # print(f'Inserting EncID into DBF at positions: {str(indexes)[1:-1]}')
        print(f'DBF state after insertion: {self._dbf.getIndexes()}')

    @property
    def filter(self):
        return self._dbf.filter

class DBFManager():
    # Constructor
    def __init__(self):
        self._dbfList = []
        self._qbf = None
        self._processStarted = time.time()
        self._cycles = 0
        self._cycleRate = 600 # how many seconds 1 DBF is to be used for
        # Create initial DBF object
        start = datetime.now()
        end = datetime.now() + timedelta(seconds=self._cycleRate)
        dbfObj = DBF(start, end)
        self._dbfList.append(dbfObj)
        
        print("#############################################################")
        print("Create DBF(" + start.strftime("%Y-%m-%d %H:%M:%S") + ", " + end.strftime("%Y-%m-%d %H:%M:%S") + ")")
        
        # Start thready for cycling DBFs
        self._dbfThread = threading.Thread(target=self.initialiseDBFCycling, name='DBF-Cycler', daemon=True)
        self._dbfThread.start()

    # Cycle DBFs every 10 minutes with no drift
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
        
        print("#############################################################")
        print("Create new DBF(" + start.strftime("%Y-%m-%d %H:%M:%S") + ", " + end.strftime("%Y-%m-%d %H:%M:%S") + ")")
        
        self._dbfList.append(DBF(start,end))
        self._cycles += 1
        if (self._cycles == 6):
            self._cycles = 0           
            self.setQBF()
            self.sendQBFToEC2Backend()
        
    # Add EncID to DBF
    def addToDBF(self, encID):
        if (self._cycles == 7):
            return

        dbfObj = self._dbfList[-1]
        start = dbfObj.startTime
        end = dbfObj.endTime
        
        print("#############################################################")
        print("Inserting " + encID.hex() + " into the DBF(" + start.strftime("%Y-%m-%d %H:%M:%S") + ", " +  end.strftime("%Y-%m-%d %H:%M:%S") + ")")
        
        dbfObj.add(encID) # add encID to current DBF

    def combineIntoQBF(self):
        return QBF(self._dbfList)
    
    def setQBF(self):
        print("#############################################################")
        print(f'Combining DBFs into a single QBF: {datetime.now()}')
        self._qbf = self.combineIntoQBF()
        print(f'Next Query Time: {datetime.now() + timedelta(hours=1)}')

    def combineIntoCBF(self):
        return CBF(self._dbfList)

    def sendQBFToEC2Backend(self):
        if (self._qbf == None):
            # print('here')
            self.setQBF()
        print("#############################################################")
        print('Uploading QBF to backend server...')
        
        # url = "http://ec2-3-26-37-172.ap-southeast-2.compute.amazonaws.com:9000/comp4337/qbf/query"
        url = "http://localhost:55000/comp4337/qbf/query"
        
        payload = self._qbf.rawJSON()
        headers = {"Content-Type": "application/json"}
        res = requests.request("POST", url, json=payload, headers=headers)
        resJSON = res.json()
        print("#############################################################")
        if (resJSON['result'] == "No Match."):
            print("QBF Uploaded to EC2 Server - Result: No Match - You are safe.")
        else:
            print("QBF Uploaded to EC2 Server - Result: Match - You are potentially at risk.")
            print("Please consult a health official, self-isolate and do a COVID-19 test at your earliest convenience.")

    def uploadCBF(self): 
        print("#############################################################")
        
        # url = "http://ec2-3-26-37-172.ap-southeast-2.compute.amazonaws.com:9000/comp4337/cbf/upload"
        url = "http://localhost:55000/comp4337/cbf/upload"
        
        payload = self.combineIntoCBF().rawJSON()
        headers = {"Content-Type": "application/json"}
        print('Uploading CBF to backend server...')
        res = requests.request("POST", url, json=payload, headers=headers)
        resJSON = res.json()
        print("#############################################################")
        if (resJSON['result'] == "Success"):
            print("CBF successfully uploaded to EC2 Server")
            self._cycles = 7 # Setting this to > 6 will disable QBF generation
            print('QBF generation has been disabled')
        else:
            print("Failed to upload CBF - rejected by EC2 Server")

    def __contains__(self, encID):
        for dbf in self._dbfList:
            if (encID in dbf):
                return True
        return False