#!/usr/bin/python           # This is server.py file

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
#READ = False
#FILENAME = ''

class a3Server(object):
    def __init__(self, cipher, IV, key):
        self.cipher = cipher
        self.IV = IV
        self.key = key
        self.READ = False
        self.FILENAME = ''
    
    def setCrypto(self):
        self.decryptor = cryptoUtil(self.key, self.IV, self.cipher)
        self.encryptor = cryptoUtil(self.key, self.IV, self.cipher)
        
    def setFileName(self, name):
        self.FILENAME = name
    
    def parseCommand(self):
        if(self.READ):
            return 'read'
        else:
            return 'write'
        
    def listenForClients(self):
        
        ip = 'localhost' 
        cSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
        cSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to make sure the connection doesn't hang   
        if(len(sys.argv) == 2):          
            Port = int(sys.argv[1]) 
            Key = ''.join(random.SystemRandom().choice(string.letters + string.digits) for i in range(32))           
        else:
            Port = int(sys.argv[1])         
            Key = sys.argv[2]
        
        cSock.bind(('', Port))            # Bind to the port
        cSock.listen(5) # Now wait for client connection.                        
        
       
        while True:
            print("Listening on port " + str(Port))  
            cli, addr = cSock.accept()       # Establish connection with client.             
            sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
            sSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            print("Using Secret Key: " + Key)
            print (time.strftime('%H:%M:%S:') + ' New Client: '+ str(addr[0]) + ' crypto: ' + self.cipher)
            self.checkCipherAndIV(cli)
            self.setCrypto()
            #print("Line 44")
            ack = self.encryptor.addPadding('ack')
            ack = self.encryptor.encrypt(ack)
            cli.send(ack)
            #cli.send(self.encryptor.encrypt('ack'))
            #print("Line 46")
            self.getCommand(cli)
            #print("Line 48")
            #cli.send("ack")
            #print("Line 50")
            self.executeCommand(cli)        
            #print("Line 52")
    
    #need to fix this such that it decrypts an incoming message properly
    #initially will be clear communication        
    def checkCipherAndIV(self, cli):
        data = cli.recv(BUFFER_SIZE,0)
        #print("Socket Started")
        data = data.decode('ascii')
        self.cipher = data
        cli.send('ack')
        data = cli.recv(BUFFER_SIZE,0)
        self.IV = b64decode(data)
        #data = data.split()         
        #self.cipher = data[0]
        #self.IV = data[1]
        #print("Line 71: ")
        #print(len(self.IV))
        #print(self.IV)
    
    #need to fix this such that it decrypts an incoming message properly
    #initially will be clear communication
    def getCommand(self,cli):
        #global READ
        #global FILENAME
        #print("Get Command:\n")
        data = cli.recv(BUFFER_SIZE,0)
        #print("Line 98: ")
        #print(data)
        data = self.decryptor.decrypt(data)
        #print(data)
        data = self.decryptor.removePadding(data)
        data = data.decode('ascii')
        data = data.split()
        if(data[0].upper() == 'read'.upper()):
            self.READ = True    
                
        self.setFileName(str(data[1]))
        print(time.strftime('%H:%M:%S:') + ' command: ' + self.parseCommand() + ' ' + self.FILENAME)
        #print(data)
        
    def executeCommand(self, cli):    
        #print("Read = " + str(self.READ))
        data = ''
        if(self.READ):
            #print("Line 105")
            fileSize = os.stat(self.FILENAME).st_size
           #print(fileSize)
            with open(self.FILENAME, 'rb') as f:
                while(f.tell() < fileSize):
                    data += f.read()
                data = self.encryptor.addPadding(data)
                    #print("line 110")
                    #print(len(data))
                data = self.encryptor.encrypt(data)
                    #print(len(data))
                    #print(data)
                cli.send(data)
                cli.close()         
        #print("line 119")
      
        elif(not self.READ):
            test = 1
            #do the stuff to write to a file
        print(time.strftime('%H:%M:%S:') + ' done')


def main():
    serv = a3Server('aes128','testIV', 'testKey')
    serv.listenForClients()
    
    
        


def validateKey(cliSock, Key):
    cliSock.send(bytearray('provide Key\n','ascii'))     
    data = cliSock.recv(BUFFER_SIZE,0)
    clientKey = data.decode('ascii').strip()
    return clientKey == Key 
    #debug messages
    #print(clientKey == Key)
        #if(clientKey == Key):
        #print("its a match")
        #print(clientKey)
        

if __name__ == '__main__':
    main()
