#!/usr/bin/python           # This is client.py file

#Name: Mike Simister
#StudentID: 10095107
#Tutorial Section: T02


import socket
import sys  
import time
import random
import string
import os
from base64 import b64encode, b64decode
from cryptoUtil import cryptoUtil

BUFFER_SIZE = 4096
READ = False
FILENAME = ''


class a3Client(object):
    def __init__(self, cipher, IV, key):
        self.cipher = cipher
        self.IV = IV
        self.key = key
    
    def setCrypto(self):
        self.decryptor = cryptoUtil(self.key, self.IV, self.cipher)
        self.encryptor = cryptoUtil(self.key, self.IV, self.cipher)

def main():
    callServer()
    
    
def callServer():
    command = sys.argv[1]
    filename = sys.argv[2]
    host_port = sys.argv[3].split(":")
    hostname = host_port[0]
    port = int(host_port[1])
    cipher = sys.argv[4]
    IV =  b64encode(os.urandom(16))
    print("Line 32:")
    print(len(IV))
    print (b64decode(IV))
    if(cipher.upper() <> "none".upper()):
        key = sys.argv[5]
    
    testInputs(command, filename, hostname, port, cipher, key)
        
    cSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
    cSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to make sure the connection doesn't hang       
    client = a3Client(cipher,b64decode(IV),key)
    client.setCrypto()
    cSock.connect((hostname,port))
    cSock.send(cipher)
    #need to encrypt/decrypt acks securely or determine
    #some type of workaround for this issue
    data = cSock.recv(1024,0)
    if(data.upper() == 'ack'.upper()):
        cSock.send(IV)
        
    data = cSock.recv(1024,0)    
    if(data.upper() == "ack".upper()):
        cSock.send(command + ' ' +  filename)
    
    receiveFile(cSock, client)
    #data = cSock.recv(1024,0)
    print("Client Line 68:")
    #print(len(data))
    #data = client.decryptor.decrypt(data)
    #print(data1)
    #data = client.decryptor.removePadding(data)
    #print(data)
  
            
def receiveFile(cSock, client):
    keepGoing = True 
    dataOut = ''   
    try:
        while keepGoing:
            data = cSock.recv(BUFFER_SIZE,0)                                     
            dataOut += data
            if not data:
                print(": line 86")
                cSock.close()
                keepGoing = False
        dataOut = client.decryptor.decrypt(dataOut)
        dataOut = client.decryptor.removePadding(dataOut)    
        print(dataOut)
                                                          
    except socket.error as t:
        if t.errno == errno.EPIPE:
            print("Client Closed")
            keepGoing = False
                
                
def testInputs(command, filename, hostname, port, cipher, key):
    print(command)
    print(filename)
    print(hostname)
    print(port)
    print(cipher)
    print(key)

        

if __name__ == '__main__':
    main()
