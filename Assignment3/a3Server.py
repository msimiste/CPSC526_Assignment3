#!/usr/bin/python           # This is server.py file

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
    listenForClients()
    
    
def listenForClients():
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
        print("Listening")  
        cli, addr = cSock.accept()       # Establish connection with client.             
        sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        sSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        print("Using Secret Key: " + Key)
        print (time.strftime('%H:%M:%S:') + ' New Client: '+ str(addr[0]) + '   crypto: ')
        checkCipherAndIV(cli)
        print("Line 44")
        cli.send("ack")
        print("Line 46")
        getCommand(cli)
        print("Line 48")
        cli.send("ack")
        print("Line 50")
        executeCommand(cli)        
        print("Line 52")
        #print(validateKey(cli,Key))
        
        
        #print(FILENAME)
        #if(validateKey(cli,Key))
            
        

        
        
def readBlock(f):
   return f.read(128)
   
def checkCipherAndIV(cli):
    data = cli.recv(BUFFER_SIZE,0)
    #print("Socket Started")
    data = data.decode('ascii')
    data = data.split()         
    print(data)

#need to fix this such that it decrypts an incoming message properly
#initially will be clear communication
def getCommand(cli):
    global READ
    global FILENAME
    print("Get Command:\n")
    data = cli.recv(BUFFER_SIZE,0)
    data = data.decode('ascii')
    data = data.split()
    if(data[0].upper() == 'read'.upper()):
        READ = True    
    FILENAME = str(data[1])
    print(data)


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
        
def executeCommand(cli):    
    print("Read = " + str(READ))
    if(True):
        print("Line 54")
        with open(FILENAME, 'rb') as f:
            data = f.read(128)
            while data:                
                cli.send(data)
                data = f.read(128)
            #print(data)
        print("line99")
      
    elif(not READ):
       test = 1
        #do the stuff to write to a file
if __name__ == '__main__':
    main()
