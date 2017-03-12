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
import hmac
import binascii


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
    IV = binascii.hexlify(os.urandom(8))
    if(cipher.upper() <> "none".upper()):
        key = sys.argv[5]
    else:
        key = "none"
    
    client = a3Client(cipher,IV,key)
    
    client.setCrypto()
    client.setParams(command,filename,hostname,port)    
    
        
    cSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
    cSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to make sure the connection doesn't hang       
    
    cSock.connect((hostname,port))
    cSock.send(cipher)
    
    #need to encrypt/decrypt acks securely or determine
    #some type of workaround for this issue
    data = cSock.recv(1024,0)
    if(data.upper() == 'ack'.upper()):
        cSock.send(IV)
    if(client.cipher.upper() <> "none".upper()):
         verifyKey(cSock, client)
             
    #send a message to test the encryption    
    data = cSock.recv(1024,0)     
    if(client.UseCipher):
        data = client.decryptor.decrypt(data)        
    
    if(data.upper() == "ack".upper()):
        msg = (command +  ' ' + filename)
        if(client.cipher.upper() <> "none".upper()):            
            msg = client.encryptor.encrypt(msg)
        cSock.send(msg)
    else:
        print("problem with Key")
        
    if(client.READ):
        receiveFile(cSock, client)
    else:
        sendFile(cSock,client,filename)

def verifyKey(cSock, client):
    hashTest = hashlib.md5()
    message = string.lowercase+string.digits+string.uppercase
    message = ''.join(random.sample(message,31)) 
    hashTest.update(message)    
    message += hashTest.hexdigest()    
    data = client.encryptor.encrypt(message)
    
    try:
        cSock.send(data)
        testData = cSock.recv(1024,0)
        #print("Line 119: " + testData)
        testData = client.decryptor.decrypt(testData)        
        msgLength = len(testData) - 32
        msg = testData[:msgLength]        
        hashOfMsg = testData[msgLength:]
        hashCheck = hashlib.md5()        
        hashCheck.update(msg)        
        hashCheck = hashCheck.hexdigest()
        validKey = hmac.compare_digest(hashCheck,hashOfMsg)
           
        if(not validKey):
            cSock.close()            
            sys.exit('Error: Invalid Key....Shutting Down Client' )            
    except ValueError as e:
        if(e.message == "Exception: The Key is Invalid"):
            print("caught error")             
            
def receiveFile(cSock, client):
    if(client.UseCipher):        
        testAck = cSock.recv(1024,0)
        testAck = client.decryptor.decrypt(testAck)       
    else:
        testAck = cSock.recv(1024,0)           
    
    ackHandler(cSock,testAck)  
    cSock.send("True") 
    keepGoing = True 
    dataOut = ''   
    try:
        while keepGoing:
            data = cSock.recv(BUFFER_SIZE,0)                                     
            dataOut += data
            if not data:                
                #cSock.close()
                keepGoing = False
        if(client.cipher.upper() <> "none".upper()):
            dataOut = client.decryptor.decrypt(dataOut)              
        sys.stdout.write(dataOut)
        cSock.close()
        sys.stdout.flush()
                                                                  
    except socket.error as t:
        if t.errno == errno.EPIPE:
            print("Client Closed")
            keepGoing = False
            
def sendFile(cSock,client,filename):
    #path = os.getcwd() + "/" + filename
    #fileSize = (str(os.path.getsize(path)))
    tempFile = sys.stdin.read() 
    fileSize = str(len(tempFile))
    if(client.cipher.upper() <> "none".upper()):        
        fileSize = client.encryptor.encrypt(fileSize)
    cSock.send(fileSize)
     
    data = cSock.recv(BUFFER_SIZE,0)
    if(client.UseCipher):
        data = client.decryptor.decrypt(data)   
    ackHandler(cSock, data) 
    #path = os.getcwd() + "/" + filename      
    #s = os.statvfs('/')
    #temp = (s.f_bavail * s.f_frsize)  / 1024
    #print(temp)
           
   
    if(client.cipher.upper() <> "none".upper()):        
        tempFile = client.encryptor.encrypt(tempFile)
    cSock.send(tempFile)
    
def ackHandler(cSock,ack):   
    if(ack.upper() == 'ack'.upper()):        
        return
    else:
        cSock.send('')
        sys.exit(ack)
    
def testInputs(command, filename, hostname, port, cipher, key):
    print(command)
    print(filename)
    print(hostname)
    print(port)
    print(cipher)
    print(key)
 

if __name__ == '__main__':
    main()
