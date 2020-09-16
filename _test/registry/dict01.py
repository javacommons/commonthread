entry = {'a': 123, 'b': 'abc'}
print(entry)
print(entry['a'])
if 'x' in entry.keys():
    print(entry['x'])
else:
    print('x dooes not exist')
print(entry.get('x', 'No-x'))
