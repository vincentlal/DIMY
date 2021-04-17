from ecdh import generateECDHObjects, verifyEphID, calcEncID
from DBF import DBFManager

if __name__ == '__main__':
    # First make some some ECDH objects
    alice, aliceEphID, aliceHash = generateECDHObjects()
    bob, bobEphID, bobHash = generateECDHObjects()
    charlie, charlieEphID, charlieHash = generateECDHObjects()
    david, davidEphID, davidHash = generateECDHObjects()
    erin, erinEphID, erinHash = generateECDHObjects()
    frank, frankEphID, frankHash = generateECDHObjects()

    assert (verifyEphID(aliceEphID, aliceHash))
    assert (verifyEphID(bobEphID, bobHash))
    assert (verifyEphID(charlieEphID, charlieHash))
    assert (verifyEphID(davidEphID, davidHash))
    assert (verifyEphID(erinEphID, erinHash))
    assert (verifyEphID(frankEphID, frankHash))

    AB_EncId = calcEncID(alice, bobEphID)
    AC_EncId = calcEncID(alice, charlieEphID)
    AD_EncId = calcEncID(alice, davidEphID)
    AE_EncId = calcEncID(alice, erinEphID)
    AF_EncId = calcEncID(alice, frankEphID)

    # Generate a bunch of random EphIDs and EncIds so we can do false positive checking
    falseEncounters = []
    for i in range (0, 1000):
        print(f'Generating false encounter {i}')
        _, randEphID, randEphIDHash = generateECDHObjects()
        assert (verifyEphID(randEphID, randEphIDHash))
        falseEncounter = calcEncID(alice, randEphID)
        falseEncounters.append(falseEncounter)

    # List of encIDs that have been stored
    # Once connected to dimy.py this will store all EncIDs collected within 10 minutes
    # But for now we will just use 5 randomly generated EncIDs for testing
    encIDs = [AB_EncId, AC_EncId, AD_EncId, AE_EncId, AF_EncId]

    dbfm = DBFManager()
    for encID in encIDs:
        dbfm.addToDBF(encID)
    
    # Check false positives
    fpCount = 0
    for fe in falseEncounters:
        if (fe in dbfm):
            fpCount += 1
    print(f'false positive count: {fpCount}')
