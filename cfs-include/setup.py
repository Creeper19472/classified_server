# -*- coding:utf-8 -*-
 
import sys, gettext, shutil 

'''
Classified Setup Wizard

A friendly wizard to setup the server. Easy-to-use.
Don't change the filename.
'''

sys.path.append('./class/common')

import colset

multicol = colset.Colset()

class setup:
    def brandnew():
        print(_('Copying files...'))
        shutil.copyfile('./class/template/config-sample.ini', '../config/config.ini')
        print(_(''))

print('Welcome to the Classified Setup Wizard!')

# Choose Languages
langlist = {
        '0': 'en_US',
        '1': 'zh_CN'
        }
print(langlist)

try:
    lang = langlist[input(multicol.Green('Please choose a language to continue the wizard: '))]
except KeyError:
    lang = 'en_US'
    print(multicol.Yellow('WARNING: Invaild language. Using the deafult language now.'))
print()

es = gettext.translation(
        'setup',
        localedir = '../locale',
        languages = [lang],
        fallback=True
        )
es.install()

# Step 1: Choose Setup Mode
print(_('Welcome to setup for the Classified File management System(CFS).'))
print(_('What do you want to do?\n\n'))
print(_('1. Brand-new installation.'))
print(_('   If you select this, we\'ll copy a new template config \
to the\n   config folder. It means ALL YOUR CHANGES WILL BE DISCARD.'))
print()
print(_('2. Update.'))
print(_('   If select this, we\'ll check updates and upgrade it.\
 It needs\n   Internet.'))
print('\n')
select = input(multicol.Green(_('Select: ')))

# Step 2: Setup
if select == '1':
    setup.brandnew()
elif select == '2':
    setup.update()
else:
    print(multicol.Red(_('ERROR: Invaild parameters!')))
    sys.exit()
