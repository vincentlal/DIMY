from DBF import DBFManager
from QBF import QBF
from bitarray import bitarray
from ecdh import generateECDHObjects, verifyEphID, calcEncID
import json

# Simplified example with small number of EncIDs

if __name__ == '__main__':
    # First make some some ECDH objects
    alice, aliceEphID = generateECDHObjects()
    bob, bobEphID = generateECDHObjects()
    charlie, charlieEphID = generateECDHObjects()
    david, davidEphID = generateECDHObjects()
    erin, erinEphID = generateECDHObjects()
    frank, frankEphID = generateECDHObjects()
    graham, grahamEphID = generateECDHObjects()

    AB_EncId = calcEncID(alice, bobEphID)
    AC_EncId = calcEncID(alice, charlieEphID)
    AD_EncId = calcEncID(alice, davidEphID)
    AE_EncId = calcEncID(alice, erinEphID)
    AF_EncId = calcEncID(alice, frankEphID)
    AG_EncId = calcEncID(alice, grahamEphID)

    # Generate a bunch of random EphIDs and EncIds so we can do false positive checking
    # falseEncounters = []
    # for i in range (0, 1000):
    #     print(f'Generating false encounter {i}')
    #     _, randEphID = generateECDHObjects()
    #     falseEncounter = calcEncID(alice, randEphID)
    #     falseEncounters.append(falseEncounter)

    encIDs = [AB_EncId, AC_EncId, AD_EncId, AE_EncId, AF_EncId, AG_EncId]
    dbfm = DBFManager()
    # Manually add one EncID to each of the bloom filters for testing combining
    dbfm.addToDBF(AB_EncId)
    dbfm.cycleDBFs() # Cycle so that all 6 are populated with 1 of the EncIDs
    dbfm.addToDBF(AC_EncId)
    dbfm.cycleDBFs()
    dbfm.addToDBF(AD_EncId)
    dbfm.cycleDBFs()
    dbfm.addToDBF(AE_EncId)
    dbfm.cycleDBFs()
    dbfm.addToDBF(AF_EncId)
    dbfm.cycleDBFs()
    dbfm.addToDBF(AG_EncId)
    for encID in encIDs:
        print(encID in dbfm) # Should print true for all
    dbfm.sendQBFToEC2Backend()
    # with open('dump2.json', 'w') as fp:
    #     fp.write(dbfm.combineIntoQBF())
    dbfm.uploadCBF()
    
    
        


