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
            print(self.key) 
            print("Using Secret Key: " + Key)
            self.key = Key
            print(self.key)
            cli, addr = cSock.accept()       # Establish connection with client.             
            sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
            sSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            
            self.checkCipherAndIV(cli)
            #self.validateKey(cli)
            self.setCrypto()
            keyValid = True
            if(self.UseCipher):
                print("line 73")                
                keyValid = self.validateKey(cli)
                print (time.strftime('%H:%M:%S:') + ' New Client: '+ str(addr[0]) + ' crypto: ' + self.cipher + ' IV: ' + b64encode(self.IV))
            else:
                print (time.strftime('%H:%M:%S:') + ' New Client: '+ str(addr[0]) + ' crypto: ' + self.cipher)
            ack = 'ack'
            if(self.cipher.upper() <> "none".upper()):
                #ack = self.encryptor.addPadding(ack)
                ack = self.encryptor.encrypt(ack)
            
            if(keyValid):
                print("Line 85")
                cli.send(ack)
                self.getCommand(cli)
                self.executeCommand(cli)  
                print("Line ")                
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
        self.setCipher()
            
    #need to fix this such that it decrypts an incoming message properly
    #initially will be clear communication
    def getCommand(self,cli):
        data = cli.recv(BUFFER_SIZE,0)
        if(self.cipher.upper() <> "none".upper()):
            data = self.decryptor.decrypt(data)
            #data = self.decryptor.removePadding(data)
        
        print(data)
        data = data.decode('ascii')
        data = data.split()
        
        if(data[0].upper() == 'read'.upper()):
            self.READ = True    
                
        self.setFileName(str(data[1]))
        ack=('ack')
        if(self.cipher.upper() <> 'none'.upper()):
            #ack = self.encryptor.addPadding(ack)
            ack = self.encryptor.encrypt(ack)
        cli.send(ack)
        print(time.strftime('%H:%M:%S:') + ' command: ' + self.parseCommand() + ' ' + self.FILENAME)
        
    def executeCommand(self, cli):  
        #cli.send('ack')  
        data = ''
        if(self.READ):
            fileSize = os.stat(self.FILENAME).st_size
            with open(self.FILENAME, 'rb') as f:
                while(f.tell() < fileSize):
                    data += f.read()
                if(self.cipher.upper() <> "none".upper()):
                    #data = self.encryptor.addPadding(data)                   
                    data = self.encryptor.encrypt(data)                    
                cli.send(data)
                cli.close()         
              
        elif(not self.READ):
            keepGoing = True
            dataOut = ''
            while keepGoing:
                #print("line 142")
                data = cli.recv(BUFFER_SIZE,0)                                     
                dataOut += data
                if not data:
                   #print(": line 86")
                    keepGoing = False
            if(self.cipher.upper() <> "none".upper()):
                dataOut = self.decryptor.decrypt(dataOut)
                #dataOut = self.decryptor.removePadding(dataOut)    
            
            fileOut = open(self.FILENAME,'w+')
            fileOut.write(dataOut)
            fileOut.flush()
            fileOut.close()
            #sys.stdout.write(dataOut)
        cli.close()    
        print(time.strftime('%H:%M:%S:') + ' done')
    
    def validateKey(self, cli):
        
        data = cli.recv(BUFFER_SIZE,0)
        data = self.decryptor.decrypt(data)
        print(data)
        #data = self.decryptor.removePadding(data)
        msgLength = len(data) - 32
        msg = data[:msgLength]
        #print("msg " + msg)
        hashOfMsg = data[msgLength:]
        hashCheck = hashlib.md5()
        #print("hashCheck1: "  + str(hashCheck))
        hashCheck.update(msg)
        #print("hashCheck2: "  + hashCheck.hexdigest())
        hashCheck = hashCheck.hexdigest()
        validKey = hmac.compare_digest(hashCheck,hashOfMsg)
        #print("line 173: " + str(hmac.compare_digest(hashCheck,hashOfMsg)))
        #print("Message: " + msg)
        #print("hashOfMsg: " + hashOfMsg)
        #print("hashCheck3: "  + hashCheck)
        #ack  = 'ack'
        #ack = self.encryptor.addPadding(ack)
        #ack = self.encryptor.encrypt(ack)
        
         #raise ValueError("The Key is Invalid")
        #cli.close()
        hashTest = hashlib.md5()
        message = string.lowercase+string.digits+string.uppercase
        message = ''.join(random.sample(message,31))
        #print(message)
        hashTest.update(message)
        #message = 'message'
        #print(message.encode("hex"))
        message += hashTest.hexdigest();
        #data = client.encryptor.addPadding(message)
        print("server side message: " + message)
        out = self.encryptor.encrypt(message)       
        cli.send(out)
        #cli.close()
        
        if (validKey):
            return True
        else:
            print ("Server side message:  invalid key")
            return False
def main():
    serv = a3Server('none','none', 'testKey')
    serv.listenForClients()
    
    
        



        

if __name__ == '__main__':
    main()
