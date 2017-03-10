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
            
        else:
            self.key = self.keyGen(16, key)
            
        
    def decrypt(self, block):        
        decryptor = AES.new(self.key,AES.MODE_CBC,self.IV)  
        block = decryptor.decrypt(block)       
        return self.simpleUnPad(block)        
        
    def encrypt(self,block):        
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
        block += ''.join(random.choice(string.letters + string.digits) for i in range(modVal))        
        if(length % 16 <> 0):
            block = block[:len(block)-1]
            block += format(modVal,'02x')[1:]
        else:
            block += '0'        
        return block
        
    def removePadding(self, block):
        padVal = int(block[-1],16)
        if(padVal == 0):
            padVal = 16
        return block[:-padVal]

    def simplePad(self, block):
        BS = 16        
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        block =  pad(block)        
        return block
        
    def simpleUnPad(self, block):
        unpad = lambda s : s[0:-ord(s[-1])]
        return unpad(block)
