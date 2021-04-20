import sys
import socket
import threading
import time
import keyexchange
  
def send(khandler):
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

    # Enable port reusage so we will be able to run multiple clients and servers on single (host, port). 
    # gpto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
   
    # for Linux >= 3.9/MacOS
    # sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # for Windows
    sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Enable broadcasting mode
    sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    minuteFlag = 0
    while True:
        if minuteFlag == 6:
            # TODO: ECDH
            khandler.genEphID()
            minuteFlag = 0
       
        # TODO: Shamir Secret Sharing
        share_in_tuple = khandler.getShareOfEphID(minuteFlag)
        message = keyexchange.shareOfEphIDToBytes(share_in_tuple)
        sender.sendto(message, ('<broadcast>', 12345))
        
        time.sleep(10)
        minuteFlag += 1
  
def receive(khandler):
    receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

    # Enable port reusage so we will be able to run multiple clients and servers on single (host, port). 
    # gpto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
   
    # for Linux >= 3.9/MacOS
    # sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # for Windows
    receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Enable broadcasting mode
    receiver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    receiver.bind(("", 12345))
    while True:
        data, addr = receiver.recvfrom(1024)
        # drop UDP packets from itself  
        if addr[0] != socket.gethostbyname(socket.gethostname()):
            # TODO: Shamir Secret Sharing
            print("received message: {} from {}".format(data, addr))
  
if __name__ == "__main__":
    khandler = keyexchange.KeyHandler()
    
    # creating thread
    t1 = threading.Thread(target=send, args=(khandler,), name='Thread-send', daemon=True)
    t2 = threading.Thread(target=receive, args=(khandler,), name='Thread-receive', daemon=True)

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
  
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()