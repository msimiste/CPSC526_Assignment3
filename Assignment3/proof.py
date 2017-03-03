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
from Crypto.Cipher import AES
from cryptoUtil import cryptoUtil
import hashlib
import hmac

BUFFER_SIZE = 4096
READ = False
FILENAME = ''

def main():
  
    key = '0123456789abcd'
    IV =  os.urandom(16)
    
    #dec = cryptoUtil(key,IV,'aes256')
    
    #plaintext = 'Mike Simister was here on friday '
    #pLen = len(plaintext)
    #print(pLen)
    #while(len(plaintext) % 16 != 0):
   #     plaintext += 'a'
    #ctext = dec.encrypt(plaintext)
    #print(ctext)
    #chopped = ctext[0:16]
    #print(chopped)
    #output = dec.decrypt(chopped)
    #out2 = dec.decrypt(ctext)
    #while(len(out2) <> pLen):
    #   out2 = out2[0:len(out2)-1]
    
    #test = dec.addPadding('mikeheremikeherem')
    #test = dec.encrypt(test)
    #print(test)
    #print(output)
    #print(out2)
    #test = dec.decrypt(test)
    #test2 = dec.removePadding(test)
    #print(test2)
    hastTest = "testing"
    hashTest = hashlib.md5()
    hashTest.update("message")
    print(hashTest.hexdigest())
    print(hashTest.digest_size)
    message = 'message'
    print(message.encode("hex"))
    
    message += hashTest.hexdigest();
    temp = len(message) - 32
    print(message)
    print(message.encode('hex'))
    print(message.encode('hex')[temp:])
    hashVal = message[temp:]
    m2 = message[:temp]
    print(hashVal)
    m3 = hashlib.md5()
    m3.update(m2)
    
    print(m2)
    print(hmac.compare_digest(hashVal,m3.hexdigest()))
    
    #keyGenTest()
        

def keyGenTest():
    dec = cryptoUtil(key,IV)
if __name__ == '__main__':
    main()
