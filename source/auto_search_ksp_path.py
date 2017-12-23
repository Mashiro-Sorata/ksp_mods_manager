import winreg

def get_tgt_name(name):
    #通过遍历键值判断是否为正确的键名，目标键名返回键名，否则返回None
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall' + '\\' +name,0,winreg.KEY_READ)
    i = 0
    while True:
        try:
            value = winreg.EnumValue(key, i)
            i += 1
            if value[1] == 'Kerbal Space Program':
                winreg.CloseKey(key)
                return name
        except OSError:
            break
    winreg.CloseKey(key)
    
def autoSearchPath():
    #遍历所有键名，通过get_tgt_name函数找到目标键名
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',0,winreg.KEY_READ)
    for i in range(0,winreg.QueryInfoKey(key)[0]-1):
        key_name = winreg.EnumKey(key,i)
        tgt_name = get_tgt_name(key_name)
        if tgt_name:
            break
    winreg.CloseKey(key)

    #如果存在目标键名，则在该键名下找到并返回信息
    if tgt_name:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall' + '\\' +tgt_name,0,winreg.KEY_READ)
        i = 0
        while True:
            try:
                value = winreg.EnumValue(key, i)
                i += 1
                if value[0] == 'InstallLocation':
                    winreg.CloseKey(key)
                    return value[1]
            except OSError:
                break
        winreg.CloseKey(key)

if __name__ == '__main__':
    print(autoSearchPath())

    

