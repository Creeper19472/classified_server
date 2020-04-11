# -*- coding: UTF-8 -*-


from Crypto.Cipher import Blowfish
import codecs
import json
import rsa

class RSA():
    def Encrypt(e, obj):
        obj = bytes(json.dumps(obj), encoding='UTF-8')
        cipher_text = rsa.encrypt(obj, e)
        return cipher_text

    def Decrypt(e, obj):
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
