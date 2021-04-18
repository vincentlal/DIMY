from ecdh import generateECDHObjects, verifyEphID, calcEncID
from DBF import DBFManager

if __name__ == '__main__':
    # First make some some ECDH objects
    alice, aliceEphID = generateECDHObjects()
    bob, bobEphID = generateECDHObjects()
    charlie, charlieEphID = generateECDHObjects()
    david, davidEphID = generateECDHObjects()
    erin, erinEphID = generateECDHObjects()
    frank, frankEphID = generateECDHObjects()

    AB_EncId = calcEncID(alice, bobEphID)
    AC_EncId = calcEncID(alice, charlieEphID)
    AD_EncId = calcEncID(alice, davidEphID)
    AE_EncId = calcEncID(alice, erinEphID)
    AF_EncId = calcEncID(alice, frankEphID)

    # Generate a bunch of random EphIDs and EncIds so we can do false positive checking
    # falseEncounters = []
    # for i in range (0, 1000):
    #     print(f'Generating false encounter {i}')
    #     _, randEphID, randEphIDHash = generateECDHObjects()
    #     falseEncounter = calcEncID(alice, randEphID)
    #     falseEncounters.append(falseEncounter)

    # List of encIDs that have been stored
    # Once connected to dimy.py this will store all EncIDs collected within 10 minutes
    # But for now we will just use 5 randomly generated EncIDs for testing
    encIDs = [AB_EncId, AC_EncId, AD_EncId, AE_EncId, AF_EncId]

    dbfm = DBFManager()
    dbfm.addToDBF(AB_EncId)
    print(dbfm._dbfList[-1]._dbf.getIndexes())
    
    # # Check false positives
    # fpCount = 0
    # for fe in falseEncounters:
    #     if (fe in dbfm):
    #         fpCount += 1
    # print(f'false positive count: {fpCount}')
