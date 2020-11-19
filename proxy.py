import os
import subprocess
import winreg
import sys
import ctypes


# proxy = sys.argv[1]


def set_key(name, value):
    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                       r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                       0, winreg.KEY_ALL_ACCESS)
    _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
    winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)

def openproxy():
    INTERNET_OPTION_REFRESH = 37
    INTERNET_OPTION_SETTINGS_CHANGED = 39
    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
    set_key('ProxyEnable', 1)
    set_key('ProxyOverride', u'*.local;<local>')  # Bypass the proxy for localhost
    set_key('ProxyServer', u'127.0.0.1:6666')


def closeproxy():
    INTERNET_OPTION_REFRESH = 37
    INTERNET_OPTION_SETTINGS_CHANGED = 39
    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
    set_key('ProxyEnable', 0)

def startmimt():
    cmd="start mitmdump -s addons.py -p 6666"
    os.system(cmd)

