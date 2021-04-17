from ecdh import generateECDHObjects, verifyEphID, calcEncID

# pip3 install simplebloomfilter
from bloomfilter import BloomFilter

# Task 6: Storing constructed EncID into Daily Bloom Filter DBF and delete the EncID

if __name__ == '__main__':
    # First make some some ECDH objects
    alice, aliceEphID, aliceHash = generateECDHObjects()
    bob, bobEphID, bobHash = generateECDHObjects()
    charlie, charlieEphID, charlieHash = generateECDHObjects()
    david, davidEphID, davidHash = generateECDHObjects()
    erin, erinEphID, erinHash = generateECDHObjects()
    frank, frankEphID, frankHash = generateECDHObjects()

    assert(verifyEphID(aliceEphID, aliceHash))
    assert (verifyEphID(bobEphID, bobHash))
    assert (verifyEphID(charlieEphID, charlieHash))
    assert (verifyEphID(davidEphID, davidHash))
    assert (verifyEphID(erinEphID, erinHash))
    assert (verifyEphID(frankEphID, frankHash))

    AB_EncId = calcEncID(alice, bobEphID)
    AC_EncId = calcEncID(alice, charlieEphID)
    AD_EncId = calcEncID(alice, davidEphID);
    AE_EncId = calcEncID(alice, erinEphID);
    AF_EncId = calcEncID(alice, frankEphID);

    # List of encIDs that have been stored
    # Once connected to dimy.py this will store all EncIDs collected within 10 minutes
    # But for now we will just use 3 of the 5randomly generated EncIDs for testing
    encIDs = [AB_EncId, AC_EncId, AD_EncId]

    # Create bloom filter (parameters set as per paper, however unable to set number of hashes)
    # Our implementation uses 17 hashes instead of 2 as described in the paper given the same false positive rate
    DBF = BloomFilter(size=800000, fp_prob=0.0000062)
    for encID in encIDs:
        DBF.add(encID)
    
    print(AB_EncId in DBF)
    print(AC_EncId in DBF)
    print(AD_EncId in DBF)
    print(AE_EncId in DBF) # not in DBF
    print(AF_EncId in DBF) # not in DBF
    

