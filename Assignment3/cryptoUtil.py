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


class cryptoUtil(object):
    condition = 'New'
    def __init__(self,key,IV):
        self.IV = IV
        self.key = key
    def decrypt(self, block):
        decryptor = AES.new(self.key,AES.MODE_CBC,self.IV)
        return decryptor.decrypt(block)
    def encrypt(self,block):
        encryptor = AES.new(self.key,AES.MODE_CBC,self.IV)
        return encryptor.encrypt(block)

#BUFFER_SIZE = 4096
#READ = False
#FILENAME = ''

#def main():
#    key = '0123456789abcdef' * 2
#    IV =  '\x00\x03' * 8
#    mode = AES.MODE_CBC
##    encryptor = AES.new(key,mode,IV=IV)
#    decryptor = AES.new(key,mode,IV=IV)
#    text = 'a' * 128    
#    ciphertext=encryptor.encrypt(text)
#    print(text)
#    print(ciphertext)
#    decrypted = decryptor.decrypt(ciphertext)
    #print('\n')
    #for i in decrypted:
        #print(i)
#    print(decrypted)
        

#if __name__ == '__main__':
#    main()
