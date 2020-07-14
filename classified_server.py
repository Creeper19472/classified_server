# -*- coding: UTF-8 -*-

VERSION = "1.4.7.799"

import sys, os, json, rsa, configparser, gettext, time, random, threading, string
import pdb

pdb.set_trace()
sys.path.append("./cfs-include/")
sys.path.append("./cfs-include/class/")
sys.path.append("./cfs-include/class/common/")
sys.path.append("./cfs-include/class/service/")

import colset, letscrypt
import connect

time1 = time.time()

def title():
    print(multicol.Yellow("______________                    _________________     _________"))
    print(multicol.Yellow("__  ____/__  /_____ _________________(_)__  __/__(_)__________  /"))
    print(multicol.Yellow("_  /    __  /_  __ `/_  ___/_  ___/_  /__  /_ __  /_  _ \  __  / "))
    print(multicol.Yellow("/ /___  _  / / /_/ /_(__  )_(__  )_  / _  __/ _  / /  __/ /_/ /  "))
    print(multicol.Yellow("\____/  /_/  \__,_/ /____/ /____/ /_/  /_/    /_/  \___/\__,_/   "))
    print(multicol.Yellow('Classified Server'), '[%s]' % VERSION)
    print()

multicol = colset.Colset()

title()
print('Running On: Python %s' % sys.version)

config = configparser.ConfigParser()
config.read('./config/config.ini')

if os.path.exists('_classified_initialized') == False:
    print(StrFormat.INFO() + 'The system is initializing, please wait ...')
    os.chdir('./secure')
    letscrypt.RSA.CreateNewKey(2048)
    os.chdir('../')
    import shutil
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
    config.set('SERVER', 'LANGUAGE', lang)
    config.write(open('./config/config.ini', 'w'))
    with open("_classified_initialized", "w") as x:
        x.write('\n')

lang = config.get("SERVER", "LANGUAGE")
es = gettext.translation(
        'cfs_server',
        localedir = 'locale',
        languages = [lang],
        fallback = True
        )
es.install()

print(StrFormat.INFO() + _("Initializing server configuration..."))

EnablePlugins = bool(config.get("PLUGIN", "EnablePlugins"))

print(StrFormat.INFO() + _("Verifying plugin information ..."))

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
            print(StrFormat.INFO() + _("Plug-in activated successfully: ") + PluginInfoConfig.get("INFO", "PLUGIN-NAME"))

connthread = threading.Thread(target=connect)
connthread.start()
time2 = time.time() - time1
print(StrFormat.INFO() + _("Done(%ss)!") % time2)

with open("./secure/e.pem", "rb") as x:
    ekey = x.read()
with open("./secure/f.pem", "rb") as x:
    fkey = x.read()

# salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
# print(letscrypt.BLOWFISH.Encrypt('aaaaaaa', salt))
