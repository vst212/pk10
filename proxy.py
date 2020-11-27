import os
import subprocess
import winreg
import sys
import ctypes
import subprocess,psutil

# proxy = sys.argv[1]
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from winproxy import ProxySetting

_translate = QtCore.QCoreApplication.translate
proc = object
def set_key(name, value):
    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                       r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                       0, winreg.KEY_ALL_ACCESS)
    _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
    winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)

def openproxy(qw):
    # 改为winproxy简单调用
    p = ProxySetting()
    p.server = dict(http='127.0.0.1:6666', https='127.0.0.1:6666')
    p.enable = True
    p.registry_write()
    # try:
    #     INTERNET_OPTION_REFRESH = 37
    #     INTERNET_OPTION_SETTINGS_CHANGED = 39
    #     internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
    #
    #
    #     set_key('ProxyEnable', 1)
    #     try:
    #         set_key('ProxyOverride', u'*.local;<local>')  # Bypass the proxy for localhost
    #     except Exception as ee:
    #         print("没有开启回环！")
    #         pass
    #     set_key('ProxyServer', u'127.0.0.1:6666')
    #     internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    #     internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
    #     qw.label.setText(_translate("wechatqrcode", "系统代理状态：已开启"))
    #
    # except Exception as  e:
    #     print(e,"出错啦！")
    #     pass


def closeproxy():
    # INTERNET_OPTION_REFRESH = 37
    # INTERNET_OPTION_SETTINGS_CHANGED = 39
    # internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
    #
    # internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    # internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
    # set_key('ProxyEnable', 0)
    p = ProxySetting()
    p.registry_read()
    p.enable = False
    p.registry_write()
    pobj = psutil.Process(proc.pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()


def startmimt(qw):
    cmd = "%s -s %s -p 6666" % ('mitmdump.exe', 'addons.py')   ##start
    global proc
    proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE,shell=False)
    # os.system(cmd)
    qw.label_2.setText(_translate("wechatqrcode", "抓取服务：已开启"))

