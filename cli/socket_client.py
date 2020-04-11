# -*- coding: UTF-8 -*-

import socket
import sys
import json
import time
import hashlib

sys.path.append("./functions/")

# import letscrypt

import pkgGenerator as cpkg


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

class MakeMsg():
    def Recv(Limit):
        Msg = client.recv(Limit)
        Msg = Msg.decode()
        return json.loads(Msg)
    
    def Send(Msg):
        byte = bytes(json.dumps(Msg), encoding='UTF-8')
        client.send(byte)

class ClientConnection():
    def MakeConnect():
        try:
            client.connect(cliinfo)
        except ConnectionRefusedError as e:
            print(e)
            return False
        MakeMsg.Send("Hi")
        if MakeMsg.Recv(64) == "Hi":
            MakeMsg.Send("Success")
        if MakeMsg.Recv(128) == "RequestAuthentication":
            ClientInfo = {
                "Agreement" : "Classified_Agreement_0",
                "ClientName" : "Client",
                "ClientVer" : "0"
                          }
            MakeMsg.Send(ClientInfo)
        TempMsg = MakeMsg.Recv(512)
        print(TempMsg)
        try:
            if TempMsg['Code'] == '10':
                print('The server needs an account and a password.')
                account = input('Account: ')
                password  = input('Password: ')
                SHA256 = hashlib.sha256(password.encode()).hexdigest()
                MakeMsg.Send(cpkg.PackagesGenerator.AuthPackage(account, SHA256))
                TempMsg = MakeMsg.Recv(128)
                print(TempMsg)
                if TempMsg['Code'] == '200':
                    print('OK. Welcome, %s!' % account)
                else:
                    print('Something wrong.')
                    if TempMsg['Code'] == '404':
                        print('Login Failed: Password incorrect.')
                    client.close()
                    return False
        except ValueError:
            pass
        '''TempMsg = MakeMsg.Recv(128)
        if TempMsg['PackageName'] == 'ActivateEncryption':
            e = TempMsg['e']
            MakeMsg.Send(letscrypt.RSA.Encrypt(e, 'OK'))
            TempCryptMsg = letscrypt.RSA.Decrypt(MakeMsg.Recv(64))
            if TempCryptMsg['Return'] == 'OK':
                KEY = TempCryptMsg['KEY']
                MakeMsg.Send(letscrypt.BLOWFISH.Encrypt('OK', KEY))'''
        return True
                


    def DisConnect():
        try:
            MakeMsg.Send("disconnect")
            if MakeMsg.Recv(64) == "disconnect":
                client.close()
            else:
                print("The server failed to respond to the client request normally, and the disconnection may be unilateral.")
        except ConnectionResetError as e:
            client.close()
            sys.exit()
        return True


cliinfo = ("127.0.0.1", 5104)

print('Connecting to the Server...')

while True:
    if ClientConnection.MakeConnect() == True:
        print('Welcome to Classified FileSystem [Pre-release 0.0.3]')
        MakeMsg.Send('VERSION')
        print('You\'re viewing the server [None], Version %s.' % MakeMsg.Recv(64))
        print('Input the filename to get the file. Type "exit" and ENTER to exit.')
        print()
        break
    else:
        print('The server send back a ConnectionRefusedError. Re-trying now.')


while True:
    cmd = input('$ ')
    if cmd != 'exit':
        MakeMsg.Send('GET ' + cmd)
        TempMsg = MakeMsg.Recv(1024)
        if TempMsg['Code'] != '200':
            print('Code '+str(TempMsg['Code'])+':')
            print(TempMsg['Message'])
        else:
            print(TempMsg['Message'])
    else:
        ClientConnection.DisConnect()
        print('221 Goodbye.')
        time.sleep(5)
        sys.exit()
