from DBF import DBFManager
from QBF import QBF
from bitarray import bitarray
from ecdh import generateECDHObjects, verifyEphID, calcEncID

# Simplified example with small number of EncIDs

if __name__ == '__main__':
    # First make some some ECDH objects
    alice, aliceEphID, aliceHash = generateECDHObjects()
    bob, bobEphID, bobHash = generateECDHObjects()
    charlie, charlieEphID, charlieHash = generateECDHObjects()
    david, davidEphID, davidHash = generateECDHObjects()
    erin, erinEphID, erinHash = generateECDHObjects()
    frank, frankEphID, frankHash = generateECDHObjects()
    graham, grahamEphID, grahamHash = generateECDHObjects()

    assert (verifyEphID(aliceEphID, aliceHash))
    assert (verifyEphID(bobEphID, bobHash))
    assert (verifyEphID(charlieEphID, charlieHash))
    assert (verifyEphID(davidEphID, davidHash))
    assert (verifyEphID(erinEphID, erinHash))
    assert (verifyEphID(frankEphID, frankHash))
    assert (verifyEphID(grahamEphID, grahamHash))

    AB_EncId = calcEncID(alice, bobEphID)
    AC_EncId = calcEncID(alice, charlieEphID)
    AD_EncId = calcEncID(alice, davidEphID)
    AE_EncId = calcEncID(alice, erinEphID)
    AF_EncId = calcEncID(alice, frankEphID)
    AG_EncId = calcEncID(alice, grahamEphID)

    # Generate a bunch of random EphIDs and EncIds so we can do false positive checking
    falseEncounters = []
    for i in range (0, 1000):
        print(f'Generating false encounter {i}')
        _, randEphID, randEphIDHash = generateECDHObjects()
        assert (verifyEphID(randEphID, randEphIDHash))
        falseEncounter = calcEncID(alice, randEphID)
        falseEncounters.append(falseEncounter)

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
    qbf = dbfm.combineIntoQBF()
    for encID in encIDs:
        print(encID in qbf) # Should print true for all


