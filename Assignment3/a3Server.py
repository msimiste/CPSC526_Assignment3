#!/usr/bin/python           # This is server.py file

#Name: Mike Simister
#StudentID: 10095107
#Tutorial Section: T02


import socket
import signal
import sys  
import time
import random
import string
import os
from base64 import b64encode, b64decode
from cryptoUtil import cryptoUtil
import hashlib
import hmac

BUFFER_SIZE = 4096

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
    
    def setCipher(self):
        self.UseCipher = (self.cipher.upper() <> "none".upper())
        
    def listenForClients(self):        
        ip = '172.19.2.81' 
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
            self.loggingMessage("Listening on port " + str(Port)) 
            self.loggingMessage("Using Secret Key: " + Key)
            self.key = Key            
            cli, addr = cSock.accept()       # Establish connection with client.             
            sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
            sSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)            
            self.checkCipherAndIV(cli)
            self.setCrypto()
            keyValid = True
            if(self.UseCipher):                               
                keyValid = self.validateKey(cli)
                if(keyValid):
                    logMsg = ' New Client: ' + str(addr[0]) + ' crypto: ' + self.cipher + ' IV: ' + self.IV
                    self.loggingMessage(logMsg)
            else:
                logMsg = ' New Client: ' + str(addr[0]) + ' crypto: ' + self.cipher
                self.loggingMessage(logMsg)                
            ack = 'ack'
            if(self.cipher.upper() <> "none".upper()):                
                ack = self.encryptor.encrypt(ack)            
            if(keyValid):                               
                cli.send(ack)                
                self.getCommand(cli)
                self.executeCommand(cli) 
                                                
    #need to fix this such that it decrypts an incoming message properly
    #initially will be clear communication        
    def checkCipherAndIV(self, cli):
        data = cli.recv(BUFFER_SIZE,0)        
        data = data.decode('ascii')
        self.cipher = data
        cli.send('ack')
        data = cli.recv(BUFFER_SIZE,0)
        #self.IV = b64decode(data)
        self.IV = data
        self.setCipher()
            
    #need to fix this such that it decrypts an incoming message properly
    #initially will be clear communication
    def getCommand(self,cli):
        data = cli.recv(BUFFER_SIZE,0)
        if(self.cipher.upper() <> "none".upper()):
            data = self.decryptor.decrypt(data)        
        data = data.decode('ascii')
        data = data.split()        
        if(data[0].upper() == 'read'.upper()):
            self.READ = True 
        else:
            self.READ = False
                
        self.setFileName(str(data[1]))                
        logMsg = ' command: ' + self.parseCommand() + ' ' + self.FILENAME
        self.loggingMessage(logMsg)
        
    def executeCommand(self, cli):         
        data = ''
                
        if(self.READ):
            path = os.getcwd() + "/" + self.FILENAME
            tempTest = os.path.isfile(path)
            self.loggingMessage(' File exists: '+ str(tempTest))
            ack = ''
            if(tempTest):
                ack=('ack')            
            else:
                ack = ("Error: That filename does not exist")
                self.loggingMessage(" Error: File does not exist")
            
            if(self.cipher.upper() <> 'none'.upper()):
                ack = self.encryptor.encrypt(ack)
        
            cli.send(ack)
            ready = bool(cli.recv(BUFFER_SIZE,0))
             
            if(tempTest and ready):
                fileSize = os.stat(self.FILENAME).st_size
                with open(self.FILENAME, 'rb') as f:
                    while(f.tell() < fileSize):
                        data += f.read()
                        if(self.cipher.upper() <> "none".upper()):                                       
                            data = self.encryptor.encrypt(data)
                        cli.send(data)                 
                    f.close()
                    cli.close()
                    
        elif(not self.READ):
            
            fileSize = cli.recv(BUFFER_SIZE,0)
            if(self.cipher.upper() <> "none".upper()):
                fileSize = self.decryptor.decrypt(fileSize)
            #print("line 152:" + str(fileSize))      
            s = os.statvfs('/')
            sizeAvail = (s.f_bavail * s.f_frsize)  / 1024 
            #print(sizeAvail)
            #sizeAvail = 50           
            hasSpace = (int(fileSize) < sizeAvail)
            if(hasSpace):
                ack = "ack"
            else:
                ack = ("Error: Filesize exceeds available space")
                self.loggingMessage("Error: Filesize exceeds available space")
                
            if(self.cipher.upper() <> "none".upper()):
                ack = self.encryptor.encrypt(ack)
            cli.send(ack)
            if(not hasSpace):
                return
                           
            keepGoing = True
            dataOut = ''
            while keepGoing:               
                data = cli.recv(BUFFER_SIZE,0)                                     
                dataOut += data
                if not data:                   
                    keepGoing = False
            if(self.cipher.upper() <> "none".upper()):
                dataOut = self.decryptor.decrypt(dataOut)                   
            fileOut = open(self.FILENAME,'w')
            fileOut.write(dataOut)
            fileOut.flush()
            fileOut.close()            
        cli.close()            
        self.loggingMessage(' done')
        
    def validateKey(self, cli):        
        data = cli.recv(BUFFER_SIZE,0)
        data = self.decryptor.decrypt(data)            
        msgLength = len(data) - 32
        msg = data[:msgLength]        
        hashOfMsg = data[msgLength:]
        hashCheck = hashlib.md5()        
        hashCheck.update(msg)        
        hashCheck = hashCheck.hexdigest()
        validKey = hmac.compare_digest(hashCheck,hashOfMsg)              
        hashTest = hashlib.md5()
        message = string.lowercase+string.digits+string.uppercase
        message = ''.join(random.sample(message,31))       
        hashTest.update(message)        
        message += hashTest.hexdigest()        
        
        out = self.encryptor.encrypt(message)       
        cli.send(out)        
        if (validKey):
            return True
        else:
            self.loggingMessage("Server side message:  invalid key")
            return False
            
    def loggingMessage(self, msg):
        print(time.strftime('%H:%M:%S:') + msg)
        
def main():
    serv = a3Server('none','none', 'testKey')
    serv.listenForClients()        

if __name__ == '__main__':
    main()
