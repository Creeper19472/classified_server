import hashlib
import sys
import shelve

Account = input('Account: ')
Password = input('Password: ')
AccessLevel = input('Level: ')
SHA256 = hashlib.sha256(Password.encode()).hexdigest()

with shelve.open('./secure/users/users.db') as db:
    db[Account] = SHA256
with shelve.open('./files/access.db') as db2:
    db2[Account] = AccessLevel
print('Done!')


