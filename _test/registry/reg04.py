# source http://itasuke.hatenablog.com/entry/2018/01/08/133510
import winreg
newkey = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r'Software\__javacommons__\abc')
newkey.Close()
winreg.DeleteKeyEx(winreg.HKEY_CURRENT_USER, r'Software\__javacommons__\abc')
