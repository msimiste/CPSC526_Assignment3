#!/usr/bin/python           # This is client.py file

#Name: Mike Simister
#StudentID: 10095107
#Tutorial Section: T02


import socket
import sys  
import time
import random
import string
from Crypto.Cipher import AES
from cryptoUtil import cryptoUtil

BUFFER_SIZE = 4096
READ = False
FILENAME = ''

def main():
  
    key = '0123456789abcdef' * 2
    IV =  '\x00\x03' * 8
    
    dec = cryptoUtil(key,IV)
    
    plaintext = 'b' * 128
    ctext = dec.encrypt(plaintext)
    print(ctext)
    chopped = ctext[0:16]
    print(chopped)
    output = dec.decrypt(chopped)
    
    print(output)
        

if __name__ == '__main__':
    main()
