# source http://itasuke.hatenablog.com/entry/2018/01/08/133510
import winreg
path = r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
with winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, path) as key:
    data, regtype = winreg.QueryValueEx(key, 'Personal')
    print('種類:', regtype)
    print('データ:', data)
