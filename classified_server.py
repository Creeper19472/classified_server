# -*- coding: UTF-8 -*-

VERSION = "[1.4.6.171]"

import sys, os, json, socket, shelve, rsa, configparser, gettext, time, random, threading, string

sys.path.append("./functions/")
sys.path.append("./functions/class/")
sys.path.append("./functions/class/common/")

import colset, letscrypt
import pkgGenerator as cpkg
from strFormat import *
from fileDetect import *

class MakeMsg:
    def Recv(conn, limit, key=None):
        if key == None:
            Msg = conn.recv(limit)
            return json.loads(Msg.decode())
        try:
            recv = json.loads(conn.recv(limit).decode())
            return letscrypt.RSA.Decrypt(recv, key)
        except:
            try:
                return letscrypt.BLOWFISH.Decrypt(recv, key)
            except:
                raise ValueError('Key is invaild')

    
    def Send(conn, Msg):
        byte = bytes(json.dumps(str(Msg)), encoding='UTF-8')
        conn.send(byte)


class ConnectThread:
    def MainThread():
        if MakeMsg.Recv(conn, 64) == "Hi":
            MakeMsg.Send(conn, "Hi")
            if MakeMsg.Recv(conn, 64) == "Success":
                print(StrFormat.INFO() + _("Connection: %s") % addr[0])
                if EnablePlugins is True:
                    for i in lists:
                        exec(i + '.connect()')
                MakeMsg.Send(conn, "RequestAuthentication")
                ClientInfo = MakeMsg.Recv(conn, 1024)
                if ClientInfo["Agreement"] != "Classified_Agreement_0":
                    print(StrFormat.WARN() + _("%s: Unable to verify client identity.") % addr[0])
                    if ForceAuthentication == "True":
                        print(StrFormat.WARN() + _("According to the security agreement, this connection has been forcibly terminated."))
                        conn.close()
                        print(StrFormat.INFO() + _("Client disconnect (%s): Forced disconnect") % addr[0])
                        sys.exit()
            else:
                print(StrFormat.WARN() + _("Exception: %s attempted to connect to the server using an invalid protocol.") % addr[0])
                conn.close()
                sys.exit()

        MakeMsg.Send(conn, cpkg.PackagesGenerator.Encrypt(fkey))
        '''EncryptMsg = MakeMsg.Recv(conn, 2048, ekey)
        if EncryptMsg['Code'] == '200':
            salt = EncryptMsg['salt']
            MakeMsg.Send(conn, cpkg.PackagesGenerator.Message(None, None), fkey)'''

        if LoginAuth == 'True':
            MakeMsg.Send(conn, cpkg.PackagesGenerator.LoginRequired())
            print(StrFormat.INFO() + _("%s: Login required") % addr[0])
            AuthInfo = MakeMsg.Recv(conn, 2048)
            try:
                if AuthInfo['Code'] == '11':
                    with shelve.open('./secure/users/users.db') as db:
                        try:
                            if AuthInfo['Password'] == db[AuthInfo['Account']]:
                                with shelve.open('./files/access.db') as fac:
                                    canaccess = fac[AuthInfo['Account']]
                                MakeMsg.Send(conn, cpkg.PackagesGenerator.Message('Login', 'success'))
                                print(StrFormat.INFO() + _("User %s Login success") % AuthInfo['Account'])
                            else:
                                raise ValueError('Password not match.')
                        except ValueError:
                            MakeMsg.Send(conn, cpkg.PackagesGenerator.FileNotFound('Login Failed'))
                            print(StrFormat.WARN() + _("User %s Failed to login") % AuthInfo['Account'])
                            conn.close()
                            sys.exit()
            except:
                MakeMsg.Send(conn, cpkg.PackagesGenerator.InternalServerError())
                print(StrFormat.WARN() + _("User undefined Failed to login"))
                conn.close()
                sys.exit()
        else:
            MakeMsg.Send(conn, cpkg.PackagesGenerator.Message('None', 'None'))

        while True: # 此处开始循环检测指令
            try:
                TempMsg = MakeMsg.Recv(conn, 1024)
                TempMsg = TempMsg.split()
                if TempMsg[0] == "disconnect":
                    if EnablePlugins is True:
                        for i in lists:
                            exec(i + '.disconnect()')
                    MakeMsg.Send(conn, "disconnect")
                    conn.close()
                    print(StrFormat.INFO() + _("Client disconnect (%s): 221 Goodbye.") % addr[0])
                    break
            except ConnectionResetError:
                    print(StrFormat.WARN() + "Client disconnect (%s): Client disconnected due to abnormal connection" % addr[0])
                    conn.close()
                    break
            except json.decoder.JSONDecodeError:
                    print('FuckU')
            if TempMsg[0] == "GET":
                try:
                    if TempMsg[1].find('../') != -1:
                        raise PermissionError('The client uses the \'../\' command')
                except (IsADirectoryError, FileNotFoundError):
                    MakeMsg.Send(conn, cpkg.PackagesGenerator.FileNotFound('File Not Found.'))
                    continue
                except PermissionError:
                    MakeMsg.Send(conn, cpkg.PackagesGenerator.InternalServerError('This request has not respose because you\'re using a hack command.'))
                    print(StrFormat.WARN() + _('%s: using the \'../\' command.') % addr[0])
                    continue
                except:
                    MakeMsg.Send(conn, cpkg.PackagesGenerator.FileNotFound())
                    continue
                try:
                    with open('./files/'+TempMsg[1], 'r') as GetFile:
                        try:
                            with shelve.open('./secure/users/access.db') as uadb:
                                if uadb[TempMsg[1]] <= canaccess:
                                    if EnablePlugins is True:
                                        for i in lists:
                                            exec(i + '.GetFile()')
                                            Result = Blocked.ReplaceBlock(GetFile.read(), canaccess)
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

            if TempMsg[0] == "Meta":
                pass


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
    print(StrFormat.INFO() + 'The system is initializing, please wait ...')
    os.chdir('./secure')
    letscrypt.RSA.CreateNewKey(2048)
    os.chdir('../')
    shutil = __import__('shutil')
    shutil.copyfile('./functions/class/template/config-sample.ini', './config/config.ini')
    langlist = {
        '0': 'en_US',
        '1': 'zh_CN',
        }
    print('欢迎使用 Classified 档案管理系统！请选择你要使用的语言：')
    print(langlist)
    try:
        lang = langlist[input('# ')]
    except KeyError:
        print('Value is invaild.')
        sys.exit()
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    config.set('SERVER', 'LANGUAGE', lang)
    config.write(open('./config/config.ini', 'w'))
    with open("_classified_initialized", "w") as x:
        x.write('\n')

config = configparser.ConfigParser()
config.read('./config/config.ini')

lang = config.get("SERVER", "LANGUAGE")
es = gettext.translation(
        'cfs_server',
        localedir = 'locale',
        languages = [lang],
        fallback = True
        )
es.install()

title()
print("[" + multicol.Green("INFO") + "] " + _("Initializing server configuration..."))

svcinfo = (config.get("SERVER", "ServerHost"), int(config.get("SERVER", "ServerPort")))
ForceAuthentication = config.get("AUTHENTICATION", "ForceAuthentication")
LoginAuth = config.get("AUTHENTICATION", "LoginAuthentication")
EnablePlugins = bool(config.get("PLUGIN", "EnablePlugins"))

server.bind(svcinfo)
server.listen(15)

print("[" + multicol.Green("INFO") + "] " + _("Verifying plugin information ..."))

if EnablePlugins is True:
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
                exec(PluginNameReplace + '.init()')
            except:
                continue
            lists.append(PluginName)
            print("[" + multicol.Green("INFO") + "] " + _("Plug-in activated successfully: ") + PluginInfoConfig.get("INFO", "PLUGIN-NAME"))
time2 = time.time() - time1
print("[" + multicol.Green("INFO") + "] " + _("Done(%ss)!") % time2)

with open("./secure/e.pem", "rb") as x:
    ekey = x.read()
with open("./secure/f.pem", "rb") as x:
    fkey = x.read()

# salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
# print(letscrypt.BLOWFISH.Encrypt('aaaaaaa', salt))

while True:
    if EnablePlugins == True:
        for i in lists:
            exec(i + '.main()')
    conn, addr = server.accept() # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
    ThreadNewName = "Thread-%s" % random.randint(1,10000)
    NewThread = MainThread(1, ThreadNewName, 1)
    NewThread.start()
