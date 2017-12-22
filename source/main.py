import wx

class MainFrame(wx.Frame):
    """
    主窗口
    """
    datas1 = {
            'D:1' : ('ksp1', 'solar1'),
            'D:2' : ('ksp2', 'solar2')
    }

    datas2 = {
            'D:3' : ('ksp3', 'solar3'),
            'D:4' : ('ksp4', 'solar4')
    }
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        
        pnl = wx.Panel(self)
        abox = wx.BoxSizer(wx.HORIZONTAL)

        self.mods_Ins = ModsList(pnl, MainFrame.datas1)
        self.mods_Unins = ModsList(pnl, MainFrame.datas2)
        self.btnAdd = wx.Button(pnl,label = '>>',size=(45,30))
        self.btnRmv = wx.Button(pnl,label = '<<',size=(45,30))
        self.btnDel = wx.Button(pnl,label = 'delete',size=(45,30))

        ins_frm = wx.StaticBox(pnl, -1, 'Installed Mods:')
        unins_frm = wx.StaticBox(pnl, -1, 'Uninstall Mods:')
        btn_frm = wx.StaticBox(pnl, -1, 'Control:')
        
        insSizer = wx.StaticBoxSizer(ins_frm, wx.HORIZONTAL)
        insbox = wx.BoxSizer(wx.HORIZONTAL)
        insbox.Add(self.mods_Ins.list)
        insSizer.Add(insbox, 0, wx.ALL|wx.CENTER, 0)

        btnSizer = wx.StaticBoxSizer(btn_frm, wx.HORIZONTAL)
        btnbox = wx.BoxSizer(wx.VERTICAL)
        btnbox.Add(self.btnAdd, 0, wx.ALL|wx.CENTER, 10)
        btnbox.Add(self.btnRmv, 0, wx.ALL|wx.CENTER, 10)
        btnbox.Add(self.btnDel, 0, wx.ALL|wx.CENTER, 10)
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
        openItem = fileMenu.Append(-1, 'Open', 'Open a mod\'s floder')
        cfgItem = fileMenu.Append(-1, 'Setting', 'Manager your mods')
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, 'File')
        menuBar.Append(helpMenu, 'Help')
        self.SetMenuBar(menuBar)
        

class ModsList:
    def __init__(self, parent, datas):
        self.list = wx.ListCtrl(parent, -1, style = wx.LC_REPORT, size=(280, 320))
        self.list.InsertColumn(0, 'Mods')
        self.list.InsertColumn(1, 'Path')
        self.list.InsertColumn(2, 'Tags')

        items = datas.items()
        for key, data in items:
            index = self.list.InsertItem(self.list.GetItemCount(), data[0])
            self.list.SetItem(index, 1, key)
            self.list.SetItem(index, 2, data[1])

        
        self.list.SetColumnWidth(0, 80)                                         #设置每一列的宽度
        self.list.SetColumnWidth(1, 100)
        self.list.SetColumnWidth(2, 100)

        

if __name__ == '__main__':
    app = wx.App()
    frm = MainFrame(None, title='KSP-Mods-Manager', size=(680,450))
    frm.Show()
    app.MainLoop()
