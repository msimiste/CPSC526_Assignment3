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
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from cryptoUtil import cryptoUtil
import hashlib


BUFFER_SIZE = 4096
READ = False
FILENAME = ''


class a3Client(object):
    def __init__(self, cipher, IV, key):
        self.cipher = cipher
        self.IV = IV
        self.key = key
        self.UseCipher = (self.cipher.upper() <> "none".upper())
            
    def setCrypto(self):
        self.decryptor = cryptoUtil(self.key, self.IV, self.cipher)
        self.encryptor = cryptoUtil(self.key, self.IV, self.cipher)
    
    def setRead(self,read):
        self.READ = read
    
    def setParams(self, command, filename, host, port):
        self.command = command
        if(command.upper() == 'read'.upper()):
            self.setRead(True)
        else:
            self.setRead(False)
        self.filename = filename
        self.host = host
        self.port = port
        
        
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
    #IV = Random.new().read(AES.block_size)
    #print("Line 32:")
    #print(len(IV))
    #print(IV)
    #print (b64decode(IV))
    if(cipher.upper() <> "none".upper()):
        key = sys.argv[5]
    else:
        key = "none"
    
    client = a3Client(cipher,b64decode(IV),key)
    #client = a3Client(cipher,IV,key)
    client.setCrypto()
    client.setParams(command,filename,hostname,port)
    
    #testInputs(command, filename, hostname, port, cipher, key)
        
    cSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
    cSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to make sure the connection doesn't hang       
    
    cSock.connect((hostname,port))
    cSock.send(cipher)
    
    #need to encrypt/decrypt acks securely or determine
    #some type of workaround for this issue
    data = cSock.recv(1024,0)
    if(data.upper() == 'ack'.upper()):
        cSock.send(IV)
       
    verifyKey(cSock, client)
    #send a message to test the encryption
    #print("line 94")
    data = cSock.recv(1024,0) 
    #print("line 95") 
    if(client.UseCipher):
        data = client.decryptor.decrypt(data)
        data = client.decryptor.removePadding(data)  
    
    if(data.upper() == "ack".upper()):
        msg = (command +  ' ' + filename)
        if(client.cipher.upper() <> "none".upper()):
            msg = client.encryptor.addPadding(msg)
            msg = client.encryptor.encrypt(msg)
        cSock.send(msg)
        
    if(client.READ):
        receiveFile(cSock, client)
    else:
        sendFile(cSock,client,filename)

def verifyKey(cSock, client):
    hashTest = hashlib.md5()
    message = string.lowercase+string.digits+string.uppercase
    message = ''.join(random.sample(message,31))
    #print(message)
    hashTest.update(message)
    message = 'message'
    #print(message.encode("hex"))
    message += hashTest.hexdigest();
    data = client.encryptor.addPadding(message)
    data = client.encryptor.encrypt(data)
    cSock.send(data)
    #retValue = cSock.recv(BUFFER_SIZE,0)
    #retValue = client.decryptor.decrypt(retValue)
    #retValue = client.decryptor.removePadding(retValue);
    #print("RetValue: " +retValue)
            
def receiveFile(cSock, client):
    if(client.UseCipher):
       testAck = cSock.recv(16,0)
       testAck = client.decryptor.decrypt(testAck)
       testAck = client.decryptor.removePadding(testAck)
       
    else:
        testAck = cSock.recv(3,0)
    
    #print("line112")
    keepGoing = True 
    dataOut = ''   
    try:
        while keepGoing:
            data = cSock.recv(BUFFER_SIZE,0)                                     
            dataOut += data
            if not data:
                #print(": line 86")
                cSock.close()
                keepGoing = False
        if(client.cipher.upper() <> "none".upper()):
            dataOut = client.decryptor.decrypt(dataOut)
            dataOut = client.decryptor.removePadding(dataOut)    
        sys.stdout.write(dataOut)
        sys.stdout.flush()
        
                                                          
    except socket.error as t:
        if t.errno == errno.EPIPE:
            print("Client Closed")
            keepGoing = False
            
def sendFile(cSock,client,filename): 
    data = cSock.recv(BUFFER_SIZE,0)
    if(client.UseCipher):
            data = client.decryptor.decrypt(data)
            data = client.decryptor.removePadding(data)
    if(data.upper() == 'ack'.upper()):
        path = os.getcwd() + "/" + filename
        #print (path)
        print(os.path.getsize(path))
        #print(os.system('df -k /'))
        s = os.statvfs('/')
        temp = (s.f_bavail * s.f_frsize)  / 1024
        print(temp)
        tempFile = sys.stdin.read()
        
    #sys.stdin.flush()
    if(client.cipher.upper() <> "none".upper()):
        tempFile = client.encryptor.addPadding(tempFile)
        tempFile = client.encryptor.encrypt(tempFile)
    cSock.send(tempFile)
    
def testInputs(command, filename, hostname, port, cipher, key):
    print(command)
    print(filename)
    print(hostname)
    print(port)
    print(cipher)
    print(key)

        

if __name__ == '__main__':
    main()
