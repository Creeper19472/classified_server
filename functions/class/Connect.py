# -*- coding: UTF-8 -*-

import sys
import socket
import json

sys.path.append("..\\functions\\")

import colset

multicol = colset.Colset()

class ConnectThread:
    def MainThread(conn, addr, lists):
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
        while True: # 此处开始循环检测指令
            TempMsg = MakeMsg.Recv(conn, 1024)
            try:
                if TempMsg == "disconnect":
                    MakeMsg.Send(conn, "disconnect")
                    conn.close()
                    print("[" + multicol.Green("INFO") + "] " + "Client disconnect", addr, ": 221 Goodbye.")
                    break
            except ConnectionResetError:
                    print("[" + multicol.Yellow("WARN") + "] " + "Client disconnect", addr, ": Client disconnected due to abnormal connection")
                    conn.close()
                    break
            if TempMsg == "VERSION":
                MakeMsg.Send(conn, VERSION)

class MakeMsg:
    def Recv(conn, Limit):
        Msg = conn.recv(Limit)
        return json.loads(Msg.decode())
    
    def Send(conn, Msg):
        byte = bytes(json.dumps(Msg), encoding='UTF-8')
        conn.send(byte)
