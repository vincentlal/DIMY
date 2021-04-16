# Testing generation of 128-bit EphID and generation of EncID

# Issue:
# 	Generating EncID requires 17byte input
# 	EphID is required to be 16 bytes
# 	Need to reconstruct a 17byte ephID at receiver end
# 		Solution:
# 			1. Use hash to determine if EphID was prepended with \x02 or \x03
# 			2. Use only one type (e.g. only EphID starting with \x02)
# 			3. Doesnt seem to actually make a difference (I dont know the maths behind ECDH) (Currently used)

# Setup:
# 	git clone https://github.com/tlsfuzzer/python-ecdsa.git
# 		into python site-packages
# 	ensure ecdsa not pip installed
# 	mv src ecdsa

from ecdsa import ECDH, SECP128r1
import hashlib

def generateECDHObjects ():
	ecdh = ECDH(curve=SECP128r1)
	ecdh.generate_private_key()
	public = ecdh.get_public_key().to_string("compressed")

	return (
		ecdh,
		public[1:],
		hashlib.md5(public).hexdigest()
	)

# load_received_public_key_bytes() requires 17 byte input
# Using solution 3
def reconstructPublic (ephID, hash):
	return b'\x02' + ephID

# Using solution 1
def reconstructPublic2 (ephID, hash):
	posEphID = b'\x03' + ephID
	negEphID = b'\x02' + ephID
	hashPosEphID = hashlib.md5(posEphID).hexdigest()
	if (hashPosEphID == hash):
		return posEphID
	else:
		return negEphID

def EphIDTest ():
	alice, aliceEphID, aliceHash = generateECDHObjects()
	bob, bobEphID, bobHash = generateECDHObjects()
	aliceReconstructed = reconstructPublic(aliceEphID, aliceHash)
	bobReconstructed = reconstructPublic(bobEphID, bobHash)

	alice.load_received_public_key_bytes(bobReconstructed)
	bob.load_received_public_key_bytes(aliceReconstructed)

	aliceEncID = alice.generate_sharedsecret_bytes()
	print(aliceEncID.hex())

	bobEncID = bob.generate_sharedsecret_bytes()
	print(bobEncID.hex())

	if (aliceEncID == bobEncID):
		print("Success!")
	else:
		print("Failure")

EphIDTest()
