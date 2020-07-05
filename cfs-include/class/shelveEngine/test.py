import shelveEngine

a = shelveEngine.shelveObj('a.db')
print(a.filepath)
print(a.shelveObj)
a.createTable('a')
a.locate('a')
a.set('av', 'be')
print(a.IsKeyExist('av'))
print(a.search('av'))
a.close()
