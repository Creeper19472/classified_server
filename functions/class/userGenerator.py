# -*- coding: UTF-8 -*-
import random, string, hashlib, sys, time
   
class Generator:
    def GenerateUser(total, length):
        usr = []
        src = string.ascii_letters + string.digits
        for x in range(0, total):
            for x in range(0, length):
                usr1 = random.sample(src, length)
            usr.append(usr1)
        return usr
        
    def GeneratePassword(total, length):
        try:
            if not length > 3 or not length < 69: # 长度必须处于列表长度范围内
                raise ValueError
        except ValueError:
            print('Exception: Length is invaild')
            sys.exit()
        src = string.ascii_letters + string.digits + '*' + '#' + '%'
        list_passwds = []
        for i in range(int(total)):
            list_passwd_all = random.sample(src, length-3) # 从字母和数字中随机取长度值
            list_passwd_all.extend(random.sample(string.digits, 1))  # 让密码中一定包含数字
            list_passwd_all.extend(random.sample(string.ascii_lowercase, 1)) # 让密码中一定包含小写字母
            list_passwd_all.extend(random.sample(string.ascii_uppercase, 1)) # 让密码中一定包含大写字母
            random.shuffle(list_passwd_all) # 打乱列表顺序
            str_passwd = ''.join(list_passwd_all) # 将列表转化为字符串
            if str_passwd not in list_passwds: # 判断是否生成重复密码
                list_passwds.append(str_passwd)
            else:
                i = i + 1
                
        return list_passwds
        
    def GenerateUserID(UserName):
        pendingText = UserName + time.asctime()
        return abs(hash(pendingText))
        
        
if __name__ == '__main__':
    UserName = input('Enter UserName: ')
    print('UserCode: ' + str(Generator.GenerateUserID(UserName)))
    Passwd = random.choice(Generator.GeneratePassword(9, 4))
    print('Password: ' + Passwd)
    print('SHA-256 PASS: ' + hashlib.sha256(Passwd.encode()).hexdigest())
    
