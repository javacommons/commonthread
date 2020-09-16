# source http://itasuke.hatenablog.com/entry/2018/01/08/133510
import winreg
path = r'Software\7-zip\FM'
key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, path, access=winreg.KEY_WRITE)
winreg.SetValueEx(key, 'JavaCommons', 0, winreg.REG_SZ, 'C:\Program Files')
#winreg.CloseKey(key)
key.Close()
