# init_config.py
# -*- coding: utf-8 -*-

#若第一次运行程序，自动检测ksp安装路径，如若没有找到，则用户手动选择路径
#第一次提示用户设定“管理文件夹”，默认为程序所在路径下的MODS文件夹

from moveFile import *
from json_builder import *
from files_operation import *

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


    
    def InitData(self):
        self.mods_Ins.Refresh()
        self.mods_Unins.Refresh()

    def InitUI(self):
        pnl = wx.Panel(self)
        abox = wx.BoxSizer(wx.HORIZONTAL)
        Bwidth = 60
        self.mods_Ins = ModsList(pnl, UNINS=False)
        self.mods_Unins = ModsList(pnl,w1=140,w2=150,w3=140)
        
        self.btnAdd = wx.Button(pnl,label = '>>',size=(Bwidth,30))
        self.btnRmv = wx.Button(pnl,label = '<<',size=(Bwidth,30))
        self.btnRefresh = wx.Button(pnl,label = 'refresh',size=(Bwidth,30))
        self.btnRun = wx.Button(pnl,label = 'run ksp', size=(Bwidth,30))

        ins_frm = wx.StaticBox(pnl, -1, 'Installed Mods:')
        unins_frm = wx.StaticBox(pnl, -1, 'Uninstalled Mods:')
        btn_frm = wx.StaticBox(pnl, -1, 'Control:')
        
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
        
        pnl.SetSizer(abox)

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
            self.Destroy()
            wx.Exit()

    def OnRclickMenu(self, event):
        self.tagsItem.Enable(True)
        self.folderItem.Enable(True)
        self.removeItem.Enable(True)    
        
        self.idlist = []
        itemid = self.list.GetFirstSelected()
        if itemid == -1:
            self.tagsItem.Enable(False)
            self.folderItem.Enable(False)
            self.removeItem.Enable(False)

        while itemid != -1:
            self.idlist.append(itemid)
            itemid = self.list.GetNextSelected(itemid)
            
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
        if dlg.ShowModal() == wx.ID_OK:
            keylist = []
            for each in self.idlist:
                keylist.append(self.list.GetItemText(each, 0))
            self.UpdateTagsInFile(keylist, dlg.GetValue())
            self.Refresh()

    def OnFolder(self, e):
        itemid = self.list.GetFirstSelected()
        path = self.list.GetItemText(itemid, 1)
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
            p = threadRMtree(pathlist)
            while p.is_alive():
                pass
            self.Refresh()
            

    def ImportMod(self):
        data = loadJson(self.datapath)
        if data.get('OldImportPath'):
            dlg = wx.DirDialog(self.parent, r'选择目标文件夹', data['OldImportPath'], style=wx.DD_DEFAULT_STYLE)
        else:
            dlg = wx.DirDialog(self.parent, r'选择目标文件夹', os.getcwd(), style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            #将此文件夹转移到mods管理目录下
            tgtpath = dlg.GetPath()
            if IsFileinFolder(tgtpath):
                SFthreadMove(tgtpath, data['Uninstalled Path'])
                data['OldImportPath'] = os.path.split(tgtpath)[0]
                saveJson(self.datapath, data)
            else:
                msgdlg = wx.MessageDialog(None, u"Mod文件夹不能为空文件夹！", u"错误", style = wx.OK | wx.ICON_HAND)
                msgdlg.ShowModal()
                msgdlg.Destroy()
        dlg.Destroy()
        self.Refresh()
        
        


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

    def OpenFolder(self, e, i):
        if i == self.InspBtn.GetId():
            tpath = self.InspText.GetValue()
            if tpath:
                dlg = wx.DirDialog(self, r'选择目标文件夹', tpath, style=wx.DD_DEFAULT_STYLE)
            else:
                dlg = wx.DirDialog(self, r'选择目标文件夹', os.getcwd(), style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.InspText.SetValue(dlg.GetPath())
        else:
            tpath = self.ModText.GetValue()
            if tpath:
                dlg = wx.DirDialog(self, r'选择目标文件夹', tpath, style=wx.DD_DEFAULT_STYLE)
            else:
                dlg = wx.DirDialog(self, r'选择目标文件夹', os.getcwd(), style=wx.DD_DEFAULT_STYLE)
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
                threadMove(self.pdata['Uninstalled Path'], newpath)

        

