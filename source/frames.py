# init_config.py
# -*- coding: utf-8 -*-

import win32api
from moveFile import *
from json_builder import *
from files_operation import *
import wx.adv
from wx.lib.wordwrap import wordwrap
import base64

class MainFrame(wx.Frame):
    """
    主窗口
    """

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.datapath = os.path.join(os.getcwd(), r'data\mainData.json')
        #pdata--PathData
        #fmdata--FolderModData
        #fidata--FolderInstalledData
        self.pdata = loadJson(self.datapath)
        _tpath = os.path.join(os.getcwd(),'KSPMods')
        if self.pdata['Uninstalled Path'] == _tpath and not os.path.exists(_tpath):
            os.mkdir(_tpath)
        self.InitUI()
        self.InitData()
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.btnRefresh)
        self.Bind(wx.EVT_BUTTON, self.OnControl_Rmove, self.btnAdd)
        self.Bind(wx.EVT_BUTTON, self.OnControl_Lmove, self.btnRmv)
        self.Bind(wx.EVT_BUTTON, self.OnRunKSP, self.btnRun)

        Icon(self).setIcon()
    
    def InitData(self):
        self.mods_Ins.Refresh()
        self.mods_Unins.Refresh()

    def InitUI(self):
        self.panel = wx.Panel(self)
        abox = wx.BoxSizer(wx.HORIZONTAL)
        Bwidth = 60
        self.mods_Ins = ModsList(self.panel, UNINS=False)
        self.mods_Unins = ModsList(self.panel,w1=140,w2=150,w3=140)
        
        self.btnAdd = wx.Button(self.panel,label = '>>',size=(Bwidth,30))
        self.btnRmv = wx.Button(self.panel,label = '<<',size=(Bwidth,30))
        self.btnRefresh = wx.Button(self.panel,label = 'refresh',size=(Bwidth,30))
        self.btnRun = wx.Button(self.panel,label = 'run ksp', size=(Bwidth,30))

        ins_frm = wx.StaticBox(self.panel, -1, 'Installed Mods:')
        unins_frm = wx.StaticBox(self.panel, -1, 'Uninstalled Mods:')
        btn_frm = wx.StaticBox(self.panel, -1, 'Control:')
        
        insSizer = wx.StaticBoxSizer(ins_frm, wx.HORIZONTAL)
        insbox = wx.BoxSizer(wx.HORIZONTAL)
        insbox.Add(self.mods_Ins.list)
        insSizer.Add(insbox, 0, wx.ALL|wx.CENTER, 0)

        btnSizer = wx.StaticBoxSizer(btn_frm, wx.HORIZONTAL)
        btnbox = wx.BoxSizer(wx.VERTICAL)
        btnbox.Add(self.btnAdd, 0, wx.ALL|wx.CENTER, 10)
        btnbox.Add(self.btnRmv, 0, wx.ALL|wx.CENTER, 10)
        btnbox.Add(self.btnRefresh, 0, wx.ALL|wx.CENTER, 10)
        btnbox.Add(self.btnRun, 0, wx.ALL|wx.CENTER, 10)
        btnSizer.Add(btnbox, 0, wx.ALL|wx.CENTER, 0)

        uninsSizer = wx.StaticBoxSizer(unins_frm, wx.HORIZONTAL)
        uninsbox = wx.BoxSizer(wx.HORIZONTAL)
        uninsbox.Add(self.mods_Unins.list)
        uninsSizer.Add(uninsbox, 0, wx.ALL|wx.CENTER, 0)

        abox.Add(uninsSizer, 0, wx.ALL|wx.CENTER, 1)
        abox.Add(btnSizer, 0, wx.ALL|wx.CENTER, 1)
        abox.Add(insSizer, 0, wx.ALL|wx.CENTER, 1)
        
        self.panel.SetSizer(abox)

        self.makeMenuBar()
        
        self.CreateStatusBar()
        self.SetStatusText("Welcome to KSP Mods Manager!")

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        importItem = fileMenu.Append(-1, 'Import', 'Import Mods to Uninstalled Path')
        cfgItem = fileMenu.Append(-1, 'Setting', 'Set your Mods\' path')
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, 'File')
        menuBar.Append(helpMenu, 'Help')
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnCfg, cfgItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnImport, importItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnAbout(self, e):
        info = wx.adv.AboutDialogInfo()
        info.SetName("About")
        info.SetVersion("V1.0")
        info.SetCopyright("      Copyright (c) 2017 Mashiro-Sorata      ")
        info.Description = wordwrap("      A tool to manager your KSP mods      ",350, wx.ClientDC(self.panel))
        info.SetWebSite("https://github.com/Mashiro-Sorata/ksp_mods_manager", "Github")
        info.Developers = ["Mashiro_Sorata"]
        info.License = wordwrap("MIT License", 500, wx.ClientDC(self.panel))
        wx.adv.AboutBox(info)


    def OnControl_Rmove(self, e):
        idlist = self.mods_Unins.getIdList()
        if idlist:
            datas = loadJson(self.datapath)
            insdata = loadJson(os.path.join(datas['Installed Path'], r'modData.json'))
            namelist = []
            for each in idlist:
                modname = self.mods_Unins.list.GetItemText(each, 0)
                insdata[modname] = [None, self.mods_Unins.list.GetItemText(each, 2)]    #path刷新时会自动重新生成
                namelist.append(modname)
            p = threadMove(datas['Uninstalled Path'], datas['Installed Path'], namelist)
            while p.is_alive():
                pass
            saveJson(os.path.join(datas['Installed Path'], r'modData.json'), insdata)
            self.InitData()
        

    def OnControl_Lmove(self, e):
        idlist = self.mods_Ins.getIdList()
        if idlist:
            datas = loadJson(self.datapath)
            uninsdata = loadJson(os.path.join(datas['Uninstalled Path'], r'modData.json'))
            namelist = []
            for each in idlist:
                modname = self.mods_Ins.list.GetItemText(each, 0)
                uninsdata[modname] = [None, self.mods_Ins.list.GetItemText(each, 2)]
                namelist.append(modname)
            p = threadMove(datas['Installed Path'], datas['Uninstalled Path'], namelist)
            while p.is_alive():
                pass
            saveJson(os.path.join(datas['Uninstalled Path'], r'modData.json'), uninsdata)
            self.InitData()

    def OnRunKSP(self, e):
        datas = loadJson(self.datapath)
        tgt = os.path.join(os.path.split(datas['Installed Path'])[0], 'KSP.exe')
        if os.path.exists(tgt):
            win32api.ShellExecute(0, 'open', tgt, '','',1)
        else:
            msgdlg = wx.MessageDialog(None, u"请检查Mods安装路径是否正确！", u"错误提示", style = wx.OK | wx.ICON_HAND)
            msgdlg.ShowModal()
            msgdlg.Destroy()


    def OnExit(self, e):
        self.Destroy()
        wx.Exit()

    def OnCfg(self, e):
        self.Destroy()
        data = loadJson(self.datapath)
        frm = CfgFrame(None, title='Settings',size=(600,300),style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        frm.InspText.SetValue(data['Installed Path'])
        frm.ModText.SetValue(data['Uninstalled Path'])
        frm.moveopt.SetValue(data['IsMove'])
        frm.Center()
        frm.Show()

    def OnImport(self, e):
        self.mods_Unins.ImportMod()
        self.InitData()

    def OnRefresh(self, e):
        self.InitData()

class ModsList:
    def __init__(self, parent, datas=None, w1=180, w2=150, w3=100, UNINS=True):
        self.parent = parent
        self.list = wx.ListCtrl(parent, -1, style = wx.LC_REPORT, size=(430, 500))
        self.datapath = os.path.join(os.getcwd(), r'data\mainData.json')
        self.UNINS = UNINS
        data = loadJson(self.datapath)
        if self.UNINS:
            try:
                self.SBT = data['SortByTags-UNINS']
            except KeyError:
                self.SBT = False
                data['SortByTags-UNINS'] = False
                saveJson(self.datapath, data)
        else:
            try:
                self.SBT = data['SortByTags-INS']
            except KeyError:
                self.SBT = False
                data['SortByTags-INS'] = False
                saveJson(self.datapath, data)
        
        self.list.InsertColumn(0, 'Mods')
        self.list.InsertColumn(1, 'Path')
        self.list.InsertColumn(2, 'Tags')

        self.list.SetColumnWidth(0, w1)                                         #设置每一列的宽度
        self.list.SetColumnWidth(1, w2)
        self.list.SetColumnWidth(2, w3)
        self.list.Bind(wx.EVT_CONTEXT_MENU, self.OnRclickMenu)
        
        #右键菜单栏
        self.menu = wx.Menu()
        if self.UNINS:
            self.importItem = self.menu.Append(-1, '导入Mods', '导入Mods')
            self.list.Bind(wx.EVT_MENU, self.OnImport, self.importItem)
            self.tagsItem = self.menu.Append(-1, '编辑Tags', '自定义修改选中项的Tags(可批量修改)')
            self.list.Bind(wx.EVT_MENU, self.OnTags, self.tagsItem)
            self.folderItem = self.menu.Append(-1, '打开文件夹', '打开选中项所在的文件夹')
            self.list.Bind(wx.EVT_MENU, self.OnFolder, self.folderItem)
            self.removeItem = self.menu.Append(-1, '删除Mods', '删除选中的Mods文件')
            self.list.Bind(wx.EVT_MENU, self.OnRemove, self.removeItem)
            self.sbtItem = self.menu.Append(-1, '按Tags排序', '将列表按照Tags重新排序')
            self.list.Bind(wx.EVT_MENU, self.OnSBT, self.sbtItem)
            self.sbmItem = self.menu.Append(-1, '按Mods排序', '将列表按照Mods重新排序')
            self.list.Bind(wx.EVT_MENU, self.OnSBM, self.sbmItem)
            
        else:
            self.tagsItem = self.menu.Append(-1, '编辑Tags', '自定义修改选中项的Tags(可批量修改)')
            self.list.Bind(wx.EVT_MENU, self.OnTags, self.tagsItem)
            self.folderItem = self.menu.Append(-1, '打开文件夹', '打开选中项所在的文件夹')
            self.list.Bind(wx.EVT_MENU, self.OnFolder, self.folderItem)
            self.removeItem = self.menu.Append(-1, '删除Mods', '删除选中的Mods文件')
            self.list.Bind(wx.EVT_MENU, self.OnRemove, self.removeItem)
            self.sbtItem = self.menu.Append(-1, '按Tags排序', '将列表按照Tags重新排序')
            self.list.Bind(wx.EVT_MENU, self.OnSBT, self.sbtItem)
            self.sbmItem = self.menu.Append(-1, '按Mods排序', '将列表按照Mods重新排序')
            self.list.Bind(wx.EVT_MENU, self.OnSBM, self.sbmItem)

        self.list.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def OnKillFocus(self, e):
        pass

    def OnSBT(self, e):
        datas = loadJson(self.datapath) 
        if self.UNINS:
            _SBT = datas['SortByTags-UNINS']
            if _SBT == True:
                return None
            datas['SortByTags-UNINS'] = True
        else:
            _SBT = datas['SortByTags-INS']
            if _SBT == True:
                return None
            datas['SortByTags-INS'] = True
        saveJson(self.datapath, datas)
        self.Refresh()

    def OnSBM(self, e):
        datas = loadJson(self.datapath)
        if self.UNINS:
            _SBT = datas['SortByTags-UNINS']
            if _SBT == False:
                return None
            datas['SortByTags-UNINS'] = False
        else:
            _SBT = datas['SortByTags-INS']
            if _SBT == False:
                return None
            datas['SortByTags-INS'] = False
        saveJson(self.datapath, datas)
        self.Refresh()

    def UpdateDataInFrame(self, datas, SortByTags=False):
        self.list.DeleteAllItems()
        if datas:
            if SortByTags:
                items = sorted(datas.items(), key = lambda item:item[1][1])
            else:
                items = sorted(datas.items(), key = lambda item:item[0])
            
            for key, data in items:
                index = self.list.InsertItem(self.list.GetItemCount(), key)
                self.list.SetItem(index, 1, data[0])
                self.list.SetItem(index, 2, data[1])

    def UpdateDataInFile(self):
        pdata = loadJson(self.datapath)
        if self.UNINS:
            _rootpath = pdata['Uninstalled Path']
        else:
            _rootpath = pdata['Installed Path']
        _filepath = os.path.join(_rootpath, 'modData.json')
        dataNew = folder2data(_rootpath)
        if os.path.exists(_filepath):
            #比较文件内数据与现在的数据，导入更新项，删除不存在的mods
            dataOld = loadJson(_filepath)
            for each in dataNew.keys():
                if dataOld.get(each):
                    dataNew[each][1] = dataOld[each][1]
        saveJson(_filepath, dataNew)
        return dataNew

    def Refresh(self):
        datas = loadJson(self.datapath)
        if self.UNINS:
            self.SBT = datas['SortByTags-UNINS']
        else:
            self.SBT = datas['SortByTags-INS']
        try:
            self.UpdateDataInFrame(self.UpdateDataInFile(), self.SBT)
        except FileNotFoundError:
            os.remove(self.datapath)
            wx.Exit()

    def getIdList(self):
        idlist = []
        itemid = self.list.GetFirstSelected()
        while itemid != -1:
            idlist.append(itemid)
            itemid = self.list.GetNextSelected(itemid)
        return idlist
        
    
    def OnRclickMenu(self, event):
        self.tagsItem.Enable(True)
        self.removeItem.Enable(True)    
        
        itemid = self.list.GetFirstSelected()
        if itemid == -1:
            self.tagsItem.Enable(False)
            self.removeItem.Enable(False)
        self.idlist = self.getIdList()
        self.list.PopupMenu(self.menu)

    def OnImport(self, e):
        self.ImportMod()

    def UpdateTagsInFile(self, keylist, tags):
        pdata = loadJson(self.datapath)
        if self.UNINS:
            _rootpath = pdata['Uninstalled Path']
        else:
            _rootpath = pdata['Installed Path']
        _filepath = os.path.join(_rootpath, 'modData.json')
        if not os.path.exists(_filepath):
            self.Refresh()
        data = loadJson(_filepath)
        for each in keylist:
            if data.get(each):
                data[each][1] = tags
        saveJson(_filepath, data)
    
    def OnTags(self, e):
        dlg = wx.TextEntryDialog(None, '输入新的Tags', 'Tags Entry')
        tag = []
        allsame = True
        for each in self.idlist:
            tag.append(self.list.GetItemText(each, 2))
            if len(tag) > 1 and tag[-1] != tag[-2]:
                allsame = False
                break
        if allsame and tag[0] != 'Undefined':
            dlg.SetValue(tag[0])
        if dlg.ShowModal() == wx.ID_OK:
            keylist = []
            for each in self.idlist:
                keylist.append(self.list.GetItemText(each, 0))
            self.UpdateTagsInFile(keylist, dlg.GetValue())
            self.Refresh()

    def OnFolder(self, e):
        itemid = self.list.GetFirstSelected()
        if itemid != -1:
            path = self.list.GetItemText(itemid, 1)
        elif self.UNINS:
            path = loadJson(self.datapath).get('Uninstalled Path')
        else:
            path = loadJson(self.datapath).get('Installed Path')
        try:
            os.startfile(path)
        except FileNotFoundError:
            self.Refresh()

    def OnRemove(self, e):
        dlg = wx.MessageDialog(None, u"是否删除所有选中的Mods？", u"警告", style = wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_YES:
            pathlist = []
            for each in self.idlist:
                pathlist.append(self.list.GetItemText(each, 1))
            passWhenAllDone(threadRMtree(pathlist))
            self.Refresh()
            

    def ImportMod(self):
        data = loadJson(self.datapath)
        if data.get('OldImportPath'):
            dlg = wx.DirDialog(None, r'选择目标文件夹', data['OldImportPath'], style=wx.DD_DEFAULT_STYLE)
        else:
            dlg = wx.DirDialog(None, r'选择目标文件夹', os.getcwd(), style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            #将此文件夹转移到mods管理目录下
            tgtpath = dlg.GetPath()
            if IsFileinFolder(tgtpath):
                p = SFthreadMove(tgtpath, data['Uninstalled Path'])
                data['OldImportPath'] = os.path.split(tgtpath)[0]
                saveJson(self.datapath, data)
                while p.is_alive():
                    pass
            else:
                msgdlg = wx.MessageDialog(None, u"Mod文件夹不能为空文件夹！", u"错误", style = wx.OK | wx.ICON_HAND)
                msgdlg.ShowModal()
                msgdlg.Destroy()
            self.Refresh()
        dlg.Destroy()
        
        
        


class CfgFrame(wx.Frame):
    """
    初始化设定窗口
    """
    def __init__(self, *args, **kw):
        super(CfgFrame, self).__init__(*args, **kw)
        self.datapath = os.path.join(os.getcwd(), r'data\mainData.json')

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.InspText = wx.TextCtrl(pnl, value=r'', size=(500,20), style = wx.TE_READONLY)
        self.InspBtn = wx.Button(pnl, label='...', size=(20,20))
        self.ModText = wx.TextCtrl(pnl, value=r'',size=(500,20), style = wx.TE_READONLY)
        self.ModBtn = wx.Button(pnl,label='...', size=(20,20))

        insCt = wx.StaticBox(pnl, -1, 'Installed Path:')
        insCtSizer = wx.StaticBoxSizer(insCt, wx.VERTICAL)
        insCtbox = wx.BoxSizer(wx.HORIZONTAL)
        insCtbox.Add(self.InspText, 0, wx.ALL | wx.CENTER, 5)
        insCtbox.Add(self.InspBtn, 0, wx.ALL | wx.CENTER, 5)
        insCtSizer.Add(insCtbox, 0, wx.ALL | wx.CENTER, 10)

        modCt = wx.StaticBox(pnl, -1, 'Uninstall Mods Path:')
        modCtSizer = wx.StaticBoxSizer(modCt, wx.VERTICAL)
        modCtbox = wx.BoxSizer(wx.HORIZONTAL)
        modCtbox.Add(self.ModText, 0, wx.ALL | wx.CENTER, 5)
        modCtbox.Add(self.ModBtn, 0, wx.ALL | wx.CENTER, 5)
        modCtSizer.Add(modCtbox, 0, wx.ALL | wx.CENTER, 10)
        
        self.moveopt = wx.CheckBox(pnl, -1, label='更改Uninstalled Mods路径时转移目录下的所有文件')
        moptSizer = wx.BoxSizer(wx.VERTICAL)
        moptSizer.Add(self.moveopt, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(moptSizer, 0, wx.ALL|wx.CENTER, 1)

        vbox.Add(insCtSizer, 0, wx.ALL|wx.CENTER, 5)
        vbox.Add(modCtSizer, 0, wx.ALL|wx.CENTER, 5)

        saveBtn = wx.Button(pnl, label='Save')
        cancelBtn = wx.Button(pnl, label='Cancel')
        scgs = wx.GridSizer(1, 2, 10, 196)
        scgs.Add(saveBtn, 0, wx.ALIGN_RIGHT, 5)
        scgs.Add(cancelBtn, 0, wx.ALIGN_LEFT, 5)
        vbox.Add(scgs, 0, wx.ALL | wx.CENTER)
        
        pnl.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, lambda e,i=self.InspBtn.GetId():self.OpenFolder(e, i), self.InspBtn)
        self.Bind(wx.EVT_BUTTON, lambda e,i=self.ModBtn.GetId():self.OpenFolder(e, i), self.ModBtn)

        self.Bind(wx.EVT_BUTTON, self.Save, saveBtn)
        self.Bind(wx.EVT_BUTTON, self.Cancel, cancelBtn)
        self.Bind(wx.EVT_CLOSE, self.Close)

        Icon(self).setIcon()

    def Close(self, e):
        if self.isCfgchange():
            dlg = wx.MessageDialog(None, u"是否保存此设置？", u"提示", style = wx.YES_NO | wx.YES_DEFAULT | wx.ICON_EXCLAMATION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Save(e)
            else:
                self.Cancel(e)
        else:
            self.Cancel(e)
                

    def OpenFolder(self, e, i):
        if i == self.InspBtn.GetId():
            tpath = self.InspText.GetValue()
            if tpath:
                dlg = wx.DirDialog(None, r'选择目标文件夹', tpath, style=wx.DD_DEFAULT_STYLE)
            else:
                dlg = wx.DirDialog(None, r'选择目标文件夹', os.getcwd(), style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.InspText.SetValue(dlg.GetPath())
        else:
            tpath = self.ModText.GetValue()
            if tpath:
                dlg = wx.DirDialog(None, r'选择目标文件夹', tpath, style=wx.DD_DEFAULT_STYLE)
            else:
                dlg = wx.DirDialog(None, r'选择目标文件夹', os.getcwd(), style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.ModText.SetValue(dlg.GetPath())
        dlg.Destroy()

    def Cancel(self, e):
        self.Destroy()
        if os.path.exists(self.datapath):
            frm = MainFrame(None, title='KSP-Mods-Manager', size=(1000,500),style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
            frm.Center()
            frm.Show()
    
    def Save(self, e):
        _path = os.path.join(os.getcwd(), r'data')
        if not os.path.exists(_path):
            os.mkdir(_path)
        data = {}
        _path = self.InspText.GetValue()
        if _path:
            if self.isCfgchange():
                data['Installed Path'] = self.InspText.GetValue()
                data['Uninstalled Path'] = self.ModText.GetValue()
                data['IsMove'] = self.moveopt.GetValue()
                if self.moveopt.GetValue():
                    self.modPathChange(data['Uninstalled Path'])
                saveJson(self.datapath, data)
            self.Destroy()
            frm = MainFrame(None, title='KSP-Mods-Manager', size=(1000,500),style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
            frm.Center()
            frm.Show()
        else:
            wx.MessageBox("Installed Path is required!", "Warning" ,wx.OK | wx.ICON_EXCLAMATION)

    def isCfgchange(self):
        olddata = loadJson(self.datapath)
        if self.InspText.GetValue() != olddata.get('Installed Path'):
            return True
        if self.ModText.GetValue() != olddata.get('Uninstalled Path'):
            return True
        if self.moveopt.GetValue() != olddata.get('IsMove'):
            return True
        return False

    def modPathChange(self, newpath):
        self.pdata = loadJson(self.datapath)
        if self.pdata:
            if newpath != self.pdata['Uninstalled Path']:
                p = threadMove(self.pdata['Uninstalled Path'], newpath)
                while p.is_alive():
                    pass
#icon
class Icon:
    filepath = os.path.join(os.getcwd(), r'data\rocket.png')
    iconB64 = b'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'

    def __init__(self, parent):
        self.creatIconFile()
        self.parent = parent

    def creatIconFile(self):
        icon = base64.b64decode(Icon.iconB64)
        if not os.path.exists(Icon.filepath):
            with open(Icon.filepath, 'wb') as f:
                f.write(icon)

    def setIcon(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(wx.Image(Icon.filepath), wx.BITMAP_TYPE_PNG))
        self.parent.SetIcon(icon)
