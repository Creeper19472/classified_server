import hashlib
import sys

sys.path.append('./cfs-include/class/shelveEngine/')

import shelveEngine

Account = input('Account: ')
Password = input('Password: ')
AccessLevel = input('Level: ')
SHA256 = hashlib.sha256(Password.encode()).hexdigest()

db = shelveEngine.shelveObj('./cfs-content/db.db')
db.locate('Users')
db.set(Account, SHA256)
db.close()
print('Done!')


