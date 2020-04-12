# -*- coding: UTF-8 -*-

VERSION = "[1.3.1.083]"

import sys, os, json, socket, shelve, rsa, configparser, time, random, threading, string

sys.path.append("./functions/")

sys.path.append("./functions/class")

from Connect import ConnectThread
import colset, letscrypt
import pkgGenerator as cpkg


class MakeMsg:
    def Recv(conn, Limit):
        Msg = conn.recv(Limit)
        return json.loads(Msg.decode())
    
    def Send(conn, Msg):
        byte = bytes(json.dumps(Msg), encoding='UTF-8')
        conn.send(byte)


class MakeMsg_ex:
    def Recv(conn, Limit):
        Msg = conn.recv(Limit)
        return Msg.decode()

    def Send(conn, Msg):
        conn.send(Msg)


class ConnectThread:
    def MainThread():
        for i in lists:
            sys.path.append(i)
            try:
                eval('__import__("' + i + '")')
            except BaseException as e:
                continue
        if MakeMsg.Recv(conn, 64) == "Hi":
            MakeMsg.Send(conn, "Hi")
            if MakeMsg.Recv(conn, 64) == "Success":
                print("[" + multicol.Green("INFO") + "] " + "Connection:", addr)
                MakeMsg.Send(conn, "RequestAuthentication")
                ClientInfo = MakeMsg.Recv(conn, 1024)
                if ClientInfo["Agreement"] != "Classified_Agreement_0":
                    print("[" + multicol.Yellow("WARN") + "] ", addr, ": Unable to verify client identity.")
                    if ForceAuthentication == "True":
                        print("[" + multicol.Yellow("WARN") + "] " + "According to the security agreement, this connection has been forcibly terminated.")
                        conn.close()
                        print("[" + multicol.Green("INFO") + "] " + "Client disconnect", addr, ": Forced disconnect")
                        sys.exit()
            else:
                print("[" + multicol.Yellow("WARN") + "] " + "Exception: ", addr, "attempted to connect to the server using an invalid protocol.")
                conn.close()
                sys.exit()
        if LoginAuth == 'True':
            MakeMsg.Send(conn, cpkg.PackagesGenerator.LoginRequired())
            print("[" + multicol.Green("INFO") + "] " + addr[0] + ": 访问阻断 要求登录")
            AuthInfo = MakeMsg.Recv(conn, 2048)
            try:
                if AuthInfo['Code'] == '11':
                    with shelve.open('./secure/users/users.db') as db:
                        try:
                            if db[AuthInfo['Account']] == AuthInfo['Password']:
                                canaccess = useraccess[AuthInfo['Account']]
                                MakeMsg.Send(conn, cpkg.PackagesGenerator.Message('Login', 'success'))
                                print("[" + multicol.Green("INFO") + "] " + "用户 %s 秘钥正确 准许登录" % AuthInfo['Account'])
                            else:
                                raise ValueError('Password not match.')
                        except ValueError:
                            MakeMsg.Send(conn, cpkg.PackagesGenerator.FileNotFound('Login Failed'))
                            print("[" + multicol.Yellow("WARN") + "]" + "用户 %s 秘钥错误 拒绝登录" % AuthInfo['Account'])
                            conn.close()
                            sys.exit()
            except:
                MakeMsg.Send(conn, cpkg.PackagesGenerator.InternalServerError())
                print("[" + multicol.Yellow("WARN") + "] " + "用户 undefined 秘钥错误 拒绝登录") 
                conn.close()
                sys.exit()
        else:
            MakeMsg.Send(conn, cpkg.PackagesGenerator.Message('None', 'None'))

        while True: # 此处开始循环检测指令
            try:
                TempMsg = MakeMsg.Recv(conn, 1024)
                TempMsg = TempMsg.split()
                if TempMsg[0] == "disconnect":
                    MakeMsg.Send(conn, "disconnect")
                    conn.close()
                    print("[" + multicol.Green("INFO") + "] " + "Client disconnect", addr, ": 221 Goodbye.")
                    break
            except ConnectionResetError:
                    print("[" + multicol.Yellow("WARN") + "] " + "Client disconnect", addr, ": Client disconnected due to abnormal connection")
                    conn.close()
                    break
            except json.decoder.JSONDecodeError:
                    print('FuckU')
            if TempMsg[0] == "GET":
                try:
                    if bool(TempMsg[1]) == False:
                        continue
                    if TempMsg[1].find('../') != -1:
                        raise
                except BaseException:
                    MakeMsg.Send(conn, cpkg.PackagesGenerator.FileNotFound('File Not Found.'))
                    continue
                try:
                    with open('./files/'+TempMsg[1], 'r') as GetFile:
                        try:
                            if fileaccessdb[TempMsg[1]] <= canaccess:
                                MakeMsg.Send(conn, cpkg.PackagesGenerator.Message('FileResult', GetFile.read()))
                            else:
                                MakeMsg.Send(conn, cpkg.PackagesGenerator.Forbidden('You don\'t have access to read this file.'))
                        except:
                            MakeMsg.Send(conn, cpkg.PackagesGenerator.Message('FileResult', GetFile.read()))
                except FileNotFoundError:
                    MakeMsg.Send(conn, cpkg.PackagesGenerator.FileNotFound('File Not Found.'))
                    continue
                except:
                    MakeMsg.Send(conn, cpkg.PackagesGenerator.InternalServerError())
                    continue

            if TempMsg[0] == "VERSION":
               MakeMsg.Send(conn, VERSION)


class MainThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        ConnectThread.MainThread()


server = socket.socket()

time1 = time.time()

def title():
    print(multicol.Yellow("______________                    _________________     _________"))
    print(multicol.Yellow("__  ____/__  /_____ _________________(_)__  __/__(_)__________  /"))
    print(multicol.Yellow("_  /    __  /_  __ `/_  ___/_  ___/_  /__  /_ __  /_  _ \  __  / "))
    print(multicol.Yellow("/ /___  _  / / /_/ /_(__  )_(__  )_  / _  __/ _  / /  __/ /_/ /  "))
    print(multicol.Yellow("\____/  /_/  \__,_/ /____/ /____/ /_/  /_/    /_/  \___/\__,_/   "))
    print(multicol.Yellow('Classified Server'), VERSION)
    print()

multicol = colset.Colset()

if os.path.exists('_classified_initialized') == False:
    print("[" + multicol.Green("INFO") + "] " + 'The system is initializing, please wait ...')
    os.chdir('./secure')
    letscrypt.RSA.CreateNewKey(2048)
    os.chdir('../')
    with open("_classified_initialized", "w") as x:
        x.write('\n')

title()
print("[" + multicol.Green("INFO") + "] " + "Initializing server configuration...")
config = configparser.ConfigParser()
config.read("./config/config.ini")

svcinfo = (config.get("SERVER", "ServerHost"), int(config.get("SERVER", "ServerPort")))
ForceAuthentication = config.get("AUTHENTICATION", "ForceAuthentication")
LoginAuth = config.get("AUTHENTICATION", "LoginAuthentication")
EnablePlugins = bool(config.get("PLUGIN", "EnablePlugins"))

fileaccessdb = shelve.open('./files/access.db')
useraccess = shelve.open('./secure/users/access.db')

server.bind(svcinfo)
server.listen(15)

print("[" + multicol.Green("INFO") + "] " + "Verifying plugin information ...")

if EnablePlugins == True:
    folders = []
    for root,dirs,files in os.walk(r"./functions/plugins/"):
        for dir in dirs:
            folders.append(os.path.join(root,dir))
    lists = []
    for i in folders:
        if eval('os.path.exists(' + '"' + i + '/info.ini' + '"' + ')') == True:
            ConfigFolderName = i + '/info.ini'
            try:
                PluginInfoConfig = configparser.ConfigParser()
                PluginInfoConfig.read(ConfigFolderName)
            except KeyError:
                continue
            sys.path.append(i)
            try:
                PluginName = PluginInfoConfig.get("INFO", "PLUGIN-NAME")
                PluginNameReplace = PluginName.replace('\'', '')
                exec('import ' + PluginNameReplace)
            except BaseException as e:
                continue
            lists.append(PluginName)
            print("[" + multicol.Green("INFO") + "] " + "Plug-in activated successfully: " + PluginInfoConfig.get("INFO", "PLUGIN-NAME"))

time2 = time.time() - time1
print("[" + multicol.Green("INFO") + "] " + ("Done(%ss)!" % time2))

with open("./secure/e.pem", "rb") as x:
    ekey = x.read()

# salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
# print(letscrypt.BLOWFISH.Encrypt('aaaaaaa', salt))

while True:
    if EnablePlugins == True:
        for i in lists:
            exec(i + '.main()')
    conn, addr = server.accept() #等待链接,多个链接的时候就会出现问题,其实返回了两个值
    ThreadNewName = "Thread-%s" % random.randint(1,10000)
    NewThread = MainThread(1, ThreadNewName, 1)
    NewThread.start()
