# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 19:05:43 2021

@author: Vazquez Montano, Axel

EE5390 - Intro to Cyber Security
Final Project
"""
" Importing Needed Libraries "
import hashlib 
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import random
import socket
import time

"Class for AES encryption algorithm"
class AEScypher(object):
    "Init function"
    def __init__(self, key):
        self.block_size = AES.block_size        #AES block size 16 bytes (128 bits)
        self.key = hashlib.sha256(key.encode()).digest()    #hash generated for key 32 bytes (256 bits)
    
    "Padding Function"
    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size    # makes sure that padded plain text is a multiple of 128
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str    # concatonating generated text to plain text
        return padded_plain_text
    
    "Encryption Function"
    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)     # padding plain text
        iv = Random.new().read(self.block_size)     #generating initialization vector
        cypher = AES.new(self.key, AES.MODE_CBC, iv)    
        encrypted_text = cypher.encrypt(plain_text.encode())    #generating encrypted text
        return b64encode(iv + encrypted_text).decode("utf-8")
    
def main():
    "Variable Initialization"
    port = 26207    # designed communication port
    pi_ip = '192.168.1.236'  # ip address of device
    key = 'this is the key'     # AES Key
    
    "Connecting to Server"
    print('Connecting to server, please wait...')
    time.sleep(3)
    client_socket = socket.socket()     # creating socket
    print('Socket created successfuly\n')
    time.sleep(3)
    client_socket.connect((pi_ip, port))    # requesting connection to server
    server_response = client_socket.recv(1024).decode()     # getting feedback on connection from server
    print (server_response)
    time.sleep(3)
    
    "Encryption of user input (message)"
    cypher_obj = AEScypher(key)     # creating an AES object
    message = input('Enter Message: ')  # user input
    encrypted_message = cypher_obj.encrypt(message) #encrypting the message from user
    time.sleep(3)
    print("\nEncrypted text: " + encrypted_message)
    time.sleep(3)
    
    "Sending Encrypted Message to Server"
    print('Sending encrypted message')
    time.sleep(3)
    client_socket.send(encrypted_message.encode())  # Sending cyphertext
    server_response = client_socket.recv(1024).decode()     # server echo 
    print (server_response)
    

if __name__ == '__main__':
    main()

