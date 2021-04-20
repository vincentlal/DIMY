import threading
import ecdh
from binascii import hexlify, unhexlify
from Crypto.Protocol.SecretSharing import Shamir

# pip install pycryptodome

def shareOfEphIDToBytes(t):
    result = ''
    for i in range(len(t)):
        if i < (len(t) - 1):
            result += str(t[i]) + ','
        else:
            result += t[i].decode('utf-8')
    # print(result.encode('utf-8'))
    return result.encode('utf-8')

class KeyHandler:
    def __init__(self):
        # multithreading part
        
        self.lock = threading.Lock()
        
        # Key generate part
        
        self.ecdhObj, self.publicKey, self.round= ecdh.generateECDHObjects()
        self.shares = Shamir.split(3, 6, self.publicKey)
        
        # task 1 & 2
        print("#############################################################")
        print("Generate EphID: " + self.publicKey.hex())
        for idx, share in self.shares:
            print("Generate share " + str(idx) + " of EphID: " + hexlify(share).decode())
        print("#############################################################")

        # Key reconstruct part
        
        ## nested dict to store shares of EphID from others
        ## peerShares[peer's IP][nth] = nth share of that Peer's EphID
        self.peerShares = {}
        
        ## nested dict to store rounds information of peer's EphID
        ## e.g. {'192.168.1.1': {'round': '1', 'status': 'accept'}}
        self.peerRound = {}
    
    def printEphID(self):
        with self.lock:
            print("Generated EphID: " + self.publicKey.hex())    

    def getShareOfEphID(self, count):
        with self.lock:
            idx, share = self.shares[count]
            print("Sending share " + str(idx) + " of EphID: " + hexlify(share).decode())
            return (self.round, idx, hexlify(share))

    def genEphID(self):
        with self.lock:
            self.ecdhObj, self.publicKey, self.round = ecdh.generateECDHObjects()
            self.shares = Shamir.split(3, 6, self.publicKey)

            # task 1 & 2
            print("#############################################################")
            print("Generate EphID: " + self.publicKey.hex())
            for idx, share in self.shares:
                print("Generate share " + str(idx) + " of EphID: " + hexlify(share).decode())
            print("#############################################################")
    
    # return EncID if enough shares are received; otherwise return None
    def addPeerShare(self, addr, data):
        with self.lock:
            data_in_str = str(data, 'UTF-8')
            peer_round, idx, share = data_in_str.split(",")
            
            # check if the peer is new
            if addr not in self.peerShares:
                # initialise self.peerShares for peer
                self.peerShares[addr] = {}
                self.peerShares[addr][idx] = share
                
                # initialise self.peerShares for peer
                self.peerRound[addr] = {}
                self.peerRound[addr]['round'] = peer_round
                self.peerRound[addr]['status'] = 'accept'
                
                return None
            else:
                # check if receiving-share and stored-shares are from same EphID
                if peer_round == self.peerRound[addr]['round']:
                    if self.peerRound[addr]['status'] == 'accept':
                        self.peerShares[addr][idx] = share
                    else:
                        return None
                else:
                    self.peerShares[addr].clear()
                    self.peerShares[addr][idx] = share
                    self.peerRound[addr]['round'] = peer_round
                    self.peerRound[addr]['status'] = 'accept'
                    return None
            
            # reconstruct peer's EphID if enough shares are received
            if len(self.peerShares[addr]) == 3:
                shares = []
                for idx, share in self.peerShares[addr].items():
                    shares.append((int(idx), unhexlify(share)))
                
                peer_ephid = Shamir.combine(shares)
                if ecdh.verifyEphID(peer_ephid, peer_round):
                    print(addr + "'s EphID verified")
                    print("Recovered EphID: " + peer_ephid.hex())
                
                encid = ecdh.calcEncID(self.ecdhObj, peer_ephid)
                print("Generate EncID: " + encid.hex())

                self.peerRound[addr]['status'] = 'ignore'
                return encid



if __name__ == "__main__":
    handler1 = KeyHandler()
    handler2 = KeyHandler()
    
    print("client1: ")
    handler1.printEphID()
    print("client2: ")
    handler2.printEphID()
    
    print()

    print("client1: ")
    handler1.addPeerShare("192.168.1.1", shareOfEphIDToBytes(handler2.getShareOfEphID(0)))
    handler1.addPeerShare("192.168.1.1", shareOfEphIDToBytes(handler2.getShareOfEphID(2)))
    handler1.addPeerShare("192.168.1.1", shareOfEphIDToBytes(handler2.getShareOfEphID(4)))

    print()

    print("client2: ")
    handler2.addPeerShare("192.168.2.1", shareOfEphIDToBytes(handler1.getShareOfEphID(1)))
    handler2.addPeerShare("192.168.2.1", shareOfEphIDToBytes(handler1.getShareOfEphID(3)))
    handler2.addPeerShare("192.168.2.1", shareOfEphIDToBytes(handler1.getShareOfEphID(5)))

    