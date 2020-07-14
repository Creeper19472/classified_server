import sys, socket, threading, configparser, pdb

pdb.set_trace()

sys.path.append('../')
sys.path.append('./cfs-include/class/shelveEngine/')
sys.path.append('../common/')

import shelveEngine
from strFormat import *
import pkgGenerator as cpkg
from fileDetect import *
import pysnooper

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
        byte = bytes(json.dumps(Msg), encoding='UTF-8')
        conn.send(byte)

@pysnooper.snoop()
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

        '''MakeMsg.Send(conn, cpkg.PackagesGenerator.Encrypt(fkey))
        EncryptMsg = MakeMsg.Recv(conn, 2048, ekey)
        if EncryptMsg['Code'] == '200':
            salt = EncryptMsg['salt']
            MakeMsg.Send(conn, cpkg.PackagesGenerator.Message(None, None), fkey)'''

        Account = 'Guest'
        if LoginAuth == 'True':
            MakeMsg.Send(conn, cpkg.PackagesGenerator.LoginRequired())
            print(StrFormat.INFO() + _("%s: Login required") % addr[0])
            AuthInfo = MakeMsg.Recv(conn, 2048)
            print(AuthInfo)
            try:
                if AuthInfo['Code'] == '11':
                    if db.IsKeyExist(AuthInfo['Account']) is False:
                        raise
                    Account = AuthInfo['Account']
                    db.search(Account)
                    print(db.search(AuthInfo['Account']))
                    if AuthInfo['Password'] == db.search(AuthInfo['Account']):
                        canaccess = 5
                        MakeMsg.Send(conn, cpkg.PackagesGenerator.Message('Login', 'success'))
                        print(StrFormat.INFO() + _("User %s Login success") % Account)
                    else:
                        raise ValueError('Password not match.')
            except:
                MakeMsg.Send(conn, cpkg.PackagesGenerator.InternalServerError())
                print(StrFormat.WARN() + _("User %s Failed to login") % Account)
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
                            with shelve.open('../../../secure/users/access.db') as uadb:
                                if uadb[TempMsg[1]] <= canaccess:
                                    if EnablePlugins is True:
                                        for i in lists:
                                            exec(i + '.GetFile()')
                                    Result = Blocked.ReplaceBlock(GetFile.read(), canaccess)
                                    MakeMsg.Send(conn, cpkg.PackagesGenerator.Message('FileResult', Result))
                                else:
                                    MakeMsg.Send(conn, cpkg.PackagesGenerator.Forbidden('You don\'t have access to read this file.'))
                        except:
                            Result = Blocked.ReplaceBlock(GetFile.read(), 5)
                            MakeMsg.Send(conn, cpkg.PackagesGenerator.Message('FileResult', Result))
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

if __name__ == '__main__':
    print('This service does not support running alone.')
    sys.exit()
    
db = shelveEngine.shelveObj('./cfs-content/db.db')
try:
    db.locate('Users')
except:
    db.createTable('Users')
    db.locate('Users')

server = socket.socket()

config = configparser.ConfigParser()
config.read('./config/config.ini')
svcinfo = (config.get("SERVER", "ServerHost"), int(config.get("SERVER", "ServerPort")))
ForceAuthentication = config.get("AUTHENTICATION", "ForceAuthentication")
LoginAuth = config.get("AUTHENTICATION", "LoginAuthentication")

server.bind(svcinfo)
server.listen(15)

while True:
    conn, addr = server.accept() # 等待链接,多个链接的时候就会出现问题,其实返回了两个值
    ThreadNewName = "Thread-%s" % random.randint(1,10000)
    NewThread = MainThread(1, ThreadNewName, 1)
    NewThread.start()
