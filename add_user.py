import hashlib
import sys
import shelve

Account = input('Account: ')
Password = input('Password: ')
SHA256 = hashlib.sha256(Password.encode()).hexdigest()

with shelve.open('./secure/users/users.db') as db:
    db[Account] = SHA256
print('Done!')


