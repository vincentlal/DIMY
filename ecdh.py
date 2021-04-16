# Testing generation of 128-bit EphID and generation of EncID

# Issue:
# 	load_received_public_key_bytes from ecdsa requires 17byte public key as input
# 		Solution:
# 			1. Use hash to determine if EphID was prepended with \x02 or \x03
# 			2. Use only one type (e.g. only EphID starting with \x02)
# 			3. Append 'b\x02' to EphID. Sign of Y does not seem to make a difference to EncID generated (Currently used)

# Setup:
# 	git clone https://github.com/tlsfuzzer/python-ecdsa.git
# 		into python site-packages
# 	ensure ecdsa not pip installed
# 	mv src ecdsa

from hashlib import md5
from ecdsa import ECDH, SECP128r1

def generateECDHObjects ():
	ecdh = ECDH(curve=SECP128r1)
	ecdh.generate_private_key()
	publicKey = ecdh.get_public_key().to_string("compressed")[1:]

	return (
		ecdh,
		publicKey,
		md5(publicKey).hexdigest()[:6]
	)

# Verify reconstructed EphID matches first 6 bytes of EphID hash from packet
def verifyEphID (EphID, receivedHash):
	return md5(EphID).hexdigest()[:6] == receivedHash

# Append with b'\x02' since required and it does not affect EncID generation
def calcEncID (ECDH, receivedEphID):
	ECDH.load_received_public_key_bytes(b'\x02' + receivedEphID)
	return ECDH.generate_sharedsecret_bytes().hex()

def EphIDTest ():
	alice, aliceEphID, aliceHash = generateECDHObjects()
	bob, bobEphID, bobHash = generateECDHObjects()

	assert (verifyEphID(aliceEphID, aliceHash))
	assert (verifyEphID(bobEphID, bobHash))

	aliceEncID = calcEncID(alice, bobEphID)
	bobEncID = calcEncID(bob, aliceEphID)

	print(aliceEncID)
	print(bobEncID)

	if (aliceEncID == bobEncID):
		print(f"Success: Generated EncID: {aliceEncID}")
	else:
		print("EncIDs not matching")

EphIDTest()
