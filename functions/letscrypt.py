# -*- coding: UTF-8 -*-


from Crypto.Cipher import Blowfish
import codecs
import json
import rsa

class RSA():
    def CreateNewKey(length):
        f, e = rsa.newkeys(length)    # 生成公钥、私钥
        e = e.save_pkcs1()  # 保存为 .pem 格式
        with open("e.pem", "wb") as x:  # 保存私钥
            x.write(e)
            x.close()
            f = f.save_pkcs1()  # 保存为 .pem 格式
        with open("f.pem", "wb") as x:  # 保存公钥
            x.write(f)
            x.close()
    
    def Encrypt(obj):
        with open("./secure/e.pem", "rb") as x:
            e = x.read()
            e = rsa.PrivateKey.load_pkcs1(e)
        with open("./secure/f.pem", "rb") as x:
            f = x.read()
            f = rsa.PublicKey.load_pkcs1(f)
        obj = bytes(json.dumps(obj), encoding='UTF-8')
        cipher_text = rsa.encrypt(obj, f)
        return cipher_text

    def Decrypt(obj):
        with open("./secure/e.pem", "rb") as x:
            e = x.read()
            e = rsa.PrivateKey.load_pkcs1(e)
        text = json.loads(rsa.decrypt(obj, e))
        return text

class BLOWFISH():
    def Encrypt(code, key):
        key = json.dumps(key)
        key = key.encode("utf-8")
        l = len(code)
        if l % 8 != 0 :
            code = code + ' ' * (8 - (l %8))#Blowfish底层决定了字符串长度必须8的整数倍，所补位空格也可以根据自己需要补位其他字符
        code = code.encode('utf-8')
        cl = Blowfish.new(key, Blowfish.MODE_ECB)
        encode = cl.encrypt(code)
        hex_encode = codecs.encode(encode, 'hex_codec')#可以根据自己需要更改hex_codec
        return hex_encode
 
    def Decrypt(string, key):
        key = key.encode("utf-8")
        string = string.encode("utf-8")
        cl = Blowfish.new(key, Blowfish.MODE_ECB)
        cipher_text = codecs.decode(string, 'hex_codec')#可以根据自己需要更改hex_codec
        code = json.loads(cl.decrypt(cipher_text))
        return "%s" % (code)
