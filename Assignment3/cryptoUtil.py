#!/usr/bin/python           # This is a helper class.py file

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
    def __init__(self,key,IV, cipher):
        self.IV = IV
        self.cipher = cipher
        if(cipher.upper() == 'aes256'.upper()):
            self.key = self.keyGen(32,key)
            #print("Line 25: " + self.key)
        else:
            self.key = self.keyGen(16, key)
            #print("Line 22: " + self.key)
        
    def decrypt(self, block):
        #print("cryptoUtil decrypt blocksize :")
        #print(len(block))
        #print("block: " + block)
        decryptor = AES.new(self.key,AES.MODE_CBC,self.IV)  
        block = decryptor.decrypt(block)
        #print("block: " + block)
        return self.simpleUnPad(block)
        #return decryptor.decrypt(block)
        
    def encrypt(self,block):
        #print("cryptoUtil encrypt blocksize :")
        #print(len(block))
        #print("line40: " + block)
        block = self.simplePad(block)
        encryptor = AES.new(self.key,AES.MODE_CBC,self.IV)
        return encryptor.encrypt(block)
        
    def keyGen(self, length, block):
        while(len(block) <> length):
               if( len(block) < length):
                   block += block
               elif(len(block) > length):
                   block = block[0:len(block)-1]
        return block
    
    def addPadding(self, block):
        length = len(block)
        if(length % 16 == 0):
            modVal = (16 - length % 16)-1
        else:
            modVal = (16 - length % 16) 
        #print(modVal)
        #while((len(block) % 16) <> 0):
         #   block += random.choice(string.letters + string.digits)
        block += ''.join(random.choice(string.letters + string.digits) for i in range(modVal))
        #print("Crypto Util - line 48")
        #print(block)
        #addedBytes = hex(modVal)
        if(length % 16 <> 0):
            block = block[:len(block)-1]
            block += format(modVal,'02x')[1:]
        else:
            block += '0'
        #print(format(modVal,'02x')[1:])
        
        #print("Crypto Util - line 64")
        #print(block)
        return block
        
    def removePadding(self, block):
        padVal = int(block[-1],16)
        if(padVal == 0):
            padVal = 16
        return block[:-padVal]

    def simplePad(self, block):
        BS = 16
        #print("Line 84 "  + block)
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        block =  pad(block)
        #print("line 86 " + block)
        return block
        
    def simpleUnPad(self, block):
        unpad = lambda s : s[0:-ord(s[-1])]
        return unpad(block)
