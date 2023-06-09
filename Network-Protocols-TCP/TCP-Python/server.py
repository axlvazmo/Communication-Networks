# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 11:48:27 2021

@author: Vazquez Montano, Axel

EE5390 - Intro to Cyber Security
Final Project
"""
" Importing Needed Libraries "
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import hashlib
import socket
import time

"Class for AES decryption algorithm"
class AEScypher(object):
    "Init function"
    def __init__(self, key):
        self.block_size = AES.block_size        #AES block size 16 bytes (128 bits)
        self.key = hashlib.sha256(key.encode()).digest()    #hash generated for key 32 bytes (256 bits)

    "Unpadding Function"
    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]   # getting the last character of the plain text
        bytes_to_remove = ord(last_character)   # getting the characters that need to be removes
        return plain_text[:-bytes_to_remove]    # returns the plain text minus the paded section 
    
    "Decryption Function"
    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)  # decoding the encrypted text
        iv = encrypted_text[:self.block_size]       # getting initialization vector
        cypher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cypher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")   # obtaining the plain text
        return self.__unpad(plain_text)     # calling the unpad function and returning the plain text only

"Function for user verification"
def user_verification(user, password):
    "Variable Initialization"
    verification = 0    # verification token, 1 is correct username and password, 0 is incorrect username and password
    username = user
    user_password = password
    password_hash = hashlib.sha256(user_password.encode()).digest() # getting the hash value from user password
    
    "*************************************************************************"
    "Generating Hash Table"
    "Passwords"
    p1 = 'ILoveHashing'
    p2 = 'ILoveCyberSecurity'
    p3 = 'ILoveAESEncryption'
    
    "Generating Hashes for All Passwords"
    hash1 = hashlib.sha256(p1.encode()).digest()
    hash2 = hashlib.sha256(p2.encode()).digest()
    hash3 = hashlib.sha256(p3.encode()).digest()
    
    "Defining hash table"
    hash_table = {'user1': hash1, 'user2': hash2, 'user3': hash3}
    "*************************************************************************"
    
    "Verification of Username and Password"
    if(username in hash_table):
        if(hash_table.get(username) == password_hash):
            verification = 1
    else:
        verification = 0
    return verification     
    
def main():
    "Variable Initialization"
    port = 26207    # designed communication port
    pi_ip = '192.168.1.236'   # ip address of device
    key = 'this is the key'     # AES Key
    display_message = 0     # variable for user verification, if 1 displais the message, if 0 it does not display message
    
    "Connecting to Client"
    server_socket = socket.socket()     # creating socket
    print('Socket created successfuly\n')
    time.sleep(3)
    server_socket.bind((pi_ip, port))   # binding to clinet
    print('Socket binded to port: ', port)
    time.sleep(3)
    server_socket.listen()  # server listening for communication
    print("Socket is listening\n")
    time.sleep(3)
    
    "Communication"
    while True:
        client, addr = server_socket.accept()   # accepting communication from client 
        print('Connection established from address = ', addr)
        time.sleep(3)
        client.send('Connected to Server'.encode())     # sending connection feedback
        message = client.recv(1024).decode()    # receiving message
        print('\nEncrypted text: ' + message + '\n')
        time.sleep(3)
        client.send('Encrypted message received'.encode())  # sending feedback on received message
        
        "Decryption and User Verification"
        cypher_obj = AEScypher(key)     # creating an AES object
        print('\n***** New Message *****')
        time.sleep(3)
        while(display_message != 1):
            "Asking for username and password"
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            
            display_message = user_verification(username, password)     # verifying if password and username are correct
            
            if(display_message):
                decrypted_message = cypher_obj.decrypt(message)     # decrypting and displaying message if username and password are correct
                print('\nNew message: ' + decrypted_message)
            else:
                print('\nIncorrect username or password, please try again')
        
        client.close()
        break
    return 0

if __name__ == '__main__':
    main()

    
    