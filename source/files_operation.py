# folder_list.py
# -*- coding: utf-8 -*-

import shutil
import os
import multiprocessing
import time
import wx

#列举所给路径下所有的非空文件夹,参数files=True则包括根目录下的文件
def enumFolder(dirpath, files=True):
    flist = []
    for each in os.listdir(dirpath):
        if not os.path.isfile(os.path.join(dirpath, each)):
            for (root, dirs, file) in os.walk(os.path .join(dirpath, each)):
                if file:
                    flist.append(each)
                    break
        elif files:
            flist.append(each)
    return flist


def folder2data(path):
    data = {}
    tag = 'undefined'
    dlist = enumFolder(path, False)
    for each in dlist:
        data[each] = (os.path.join(path,each), tag)
    return data


#通过same参数返回两个路径下相同或者不同的文件名列表
def listFilesBySorD(oldpath, newpath, same=True):
    flist = []
    #t2
    oldlist = enumFolder(oldpath)
    newlist = os.listdir(newpath)
    if same:
        for each in oldlist:
            if each in newlist:
                flist.append(each)
    else:
        for each in oldlist:
            if each not in newlist:
                flist.append(each)
    return flist

    

#转移某个文件夹下所有文件(包括文件夹)
def moveFinF(oldpath, newpath, oldfilelist=None):
    if oldfilelist:
        flist = oldfilelist
    else:
        #t1
        flist = enumFolder(oldpath)
    for each in flist:
        try:
            print(each)
            shutil.move(os.path.join(oldpath,each),newpath)
        except shutil.Error:
            continue

#删除给出路径下在nlist列表中的文件
def rmtreeByNamelist(rootpath, nlist):
    for each in nlist:
        eachpath = os.path.join(rootpath, each)
        if os.path.isfile(eachpath):
            os.remove(eachpath)
        else:
            shutil.rmtree(os.path.join(rootpath, each))

def threadMove(oldpath, newpath):
    samefiles = listFilesBySorD(oldpath, newpath)
    if samefiles:
        dlg = wx.MessageDialog(None, u"检测到有相同文件，是否覆盖？", u"警告", style = wx.YES_NO | wx.YES_DEFAULT | wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_YES:
            rmtreeByNamelist(newpath, samefiles)
            p = multiprocessing.Process(target=moveFinF, args=(oldpath, newpath))
            p.start()
            moveDialog(oldpath)
        else:
            difffiles = listFilesBySorD(oldpath, newpath, same=False)
            p = multiprocessing.Process(target=moveFinF, args=(oldpath, newpath, difffiles))
            p.start()
            moveDialog(oldpath, dlist=difffiles)
    else:
        p = multiprocessing.Process(target=moveFinF, args=(oldpath, newpath))
        p.start()
        moveDialog(oldpath)

def moveDialog(oldpath, dlist=None):
    allsize = getDirSize(oldpath, dlist)
    #文件大于5M则显示dialog进度条
    if allsize > 5242880 :
        msg = 'Loading...\n文件转移中...'
        dialog = wx.ProgressDialog("文件转移", msg,100,style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        alive = True
        percent = 0
        while alive and percent < 100:
            leftsize = getDirSize(oldpath, dlist)
            percent = ((allsize-leftsize)/allsize)*100
            if percent == 100:
                msg = 'Mods转移完成！'
            #wx.Sleep(0.3)
            alive = dialog.Update(percent, newmsg=msg)
        dialog.Destroy()

#获得路径下列表中的所有文件目录的大小
def getDirSize(dirpath, nlist=None):
    size = 0
    if not nlist:
        for (root,dirs,files) in os.walk(dirpath):
            for name in files:
                try:
                    size += os.path.getsize(os.path.join(root, name))
                except:
                    continue
    else:
        for each in nlist:
            size += getDirSize(os.path.join(dirpath, each))
    return size
        

if __name__ == '__main__':
    path = r'E:\Work\python-learn\project\ksp_mods_manager\prj'
    print(os.path.isfile(os.path.join(path, 'frames - 副本.py')))
    print(enumFolder(path,False))
    
