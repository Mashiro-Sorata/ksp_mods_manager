# main.py
# -*- coding: utf-8 -*-

from auto_search_ksp_path import *
from frames import *

"""
    数据存放方式
    datas = {
            'mod name' : ('path', 'tags'),
            ...
    }
"""

if __name__ == '__main__':
    app = wx.App()

    if not os.path.isfile(os.path.join(os.getcwd(),r'data\mainData.json')):
        #初始化设定(Default)
        inspath = os.path.join(autoSearchPath(),'GameData')
        frm1 = CfgFrame(None, title='Settings',size=(600,300),style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        if inspath:
            frm1.InspText.SetValue(inspath)
        frm1.ModText.SetValue(os.path.join(os.getcwd(),'KSPMods'))
        frm1.Center()
        frm1.Show()
    else:
        frm = MainFrame(None, title='KSP-Mods-Manager', size=(1000,500),style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        frm.Center()
        frm.Show()
        
    app.MainLoop()
