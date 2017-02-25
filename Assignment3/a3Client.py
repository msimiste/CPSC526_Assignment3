#!/usr/bin/python           # This is client.py file

#Name: Mike Simister
#StudentID: 10095107
#Tutorial Section: T02


import socket
import sys  
import time
import random
import string

BUFFER_SIZE = 4096
READ = False
FILENAME = ''

def main():
    callServer()
    
    
def callServer():
    command = sys.argv[1]
    filename = sys.argv[2]
    host_port = sys.argv[3].split(":")
    hostname = host_port[0]
    port = int(host_port[1])
    cipher = sys.argv[4]
    if(cipher.upper() <> "none".upper()):
        key = sys.argv[5]
    
    testInputs(command, filename, hostname, port, cipher, key)
        
    cSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
    cSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to make sure the connection doesn't hang       
    
    cSock.connect((hostname,port))
    cSock.send(cipher + " test ")
    data = cSock.recv(1024,0)    
    if(data.upper() == "ack".upper()):
        cSock.send(command + ' ' +  filename)
    data = cSock.recv(1024,0)
    print(data)
    data = cSock.recv(1024,0)
    print(data)
    
    
   
    #while True:
     #   print("Listening")  
      ## sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        #sSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        #print("Using Secret Key: " + Key)
   #     print (time.strftime('%H:%M:%S:') + ' New Client: '+ str(addr[0]) + '   crypto: ')
   #     checkCipherAndIV(cli)
    #    getCommand(cli)
     #   executeCommand(cli)        
      #  print("Line 45")
        #print(validateKey(cli,Key))
        
        
        #print(FILENAME)
        #if(validateKey(cli,Key))
            
        
def testInputs(command, filename, hostname, port, cipher, key):
    print(command)
    print(filename)
    print(hostname)
    print(port)
    print(cipher)
    print(key)

        

if __name__ == '__main__':
    main()
