import pickle
import winreg
import json
entry = {'a': 123, 'b': 'abc'}
with open('entry.tmp', 'wb') as f:
    pickle.dump(entry, f)
with open('entry.tmp', 'rb') as f:
    entry2 = pickle.load(f)
print(entry2)
b = pickle.dumps(entry)
print(b)
with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r'SOFTWARE\__javacommons__\pickle') as key:
    winreg.SetValueEx(key, None, 0, winreg.REG_BINARY, b)
with winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r'SOFTWARE\__javacommons__\pickle') as key:
    data, regtype = winreg.QueryValueEx(key, None)
    print('種類:', regtype)
    print('データ:', data)
print(data)
entry3 = pickle.loads(data)
print(entry3)
with open('entry.json', mode='w', encoding='utf-8') as f:
    json.dump(entry, f, indent=2)
with open('entry.json', 'r', encoding='utf-8') as f:
    entry4 = json.load(f)
print(entry4)
