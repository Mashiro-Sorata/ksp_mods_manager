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

def IsFileinFolder(path):
    for (root, dirs, file) in os.walk(path):
        if file:
            return True
    return False

def folder2data(path):
    data = {}
    tag = 'Undefined'
    dlist = enumFolder(path, False)
    for each in dlist:
        data[each] = [os.path.join(path,each), tag]
    return data


#通过same参数返回两个路径下相同或者不同的文件名列表
def listFilesBySorD(oldpath, newpath, filenamelist=None):
    samelist = []
    difflist = []
    newlist = os.listdir(newpath)
    if filenamelist == None:
        oldlist = enumFolder(oldpath)
        for each in oldlist:
            if each in newlist:
                samelist.append(each)
            else:
                difflist.append(each)
    else:
        for each in filenamelist:
            if each in newlist:
                samelist.append(each)
            else:
                difflist.append(each)
    return (samelist, difflist)

    

#转移某个文件夹下所有文件(包括文件夹)
def moveFinF(oldpath, newpath, oldfilelist=None, samefile=None, override=False):
    if samefile and override:
        rmtreeByNamelist(newpath, samefile)
    elif not samefile and override:
        raise Exception("Wrong args!'override' can not be True when 'samefiles' is empty!")
        
    if oldfilelist != None:
        flist = oldfilelist
    else:
        flist = enumFolder(oldpath)
    for each in flist:
        try:
            shutil.move(os.path.join(oldpath,each),newpath)
        except shutil.Error:
            pass

#删除给出路径下在nlist列表中的文件
def rmtreeByNamelist(rootpath, nlist):
    for each in nlist:
        eachpath = os.path.join(rootpath, each)
        if os.path.isfile(eachpath):
            os.remove(eachpath)
        else:
            shutil.rmtree(os.path.join(rootpath, each))
        

#转移oldpath下所有非空文件(可通过filenamelist选择)
def threadMove(oldpath, newpath, filenamelist=None):
    (samefiles, difffiles) = listFilesBySorD(oldpath, newpath, filenamelist)
    if samefiles:
        dlg = wx.MessageDialog(None, u"检测到有相同文件，是否覆盖？", u"警告", style = wx.YES_NO | wx.YES_DEFAULT | wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_YES:
            p = multiprocessing.Process(target=moveFinF, args=(oldpath, newpath, filenamelist, samefiles, True))
            p.start()
            moveDialog(oldpath, dlist=filenamelist)
        else:
            p = multiprocessing.Process(target=moveFinF, args=(oldpath, newpath, difffiles))
            p.start()
            moveDialog(oldpath, dlist=difffiles)
    else:
        p = multiprocessing.Process(target=moveFinF, args=(oldpath, newpath, filenamelist))
        p.start()
        moveDialog(oldpath, dlist=filenamelist)
    return p

def moveDialog(oldpath, dlist=None):
    allsize = getDirSize(oldpath, dlist)
    #文件大于5M则显示dialog进度条
    if allsize > 5242880 :
        msg = 'Loading...\n文件转移中，请稍等...'
        dialog = wx.ProgressDialog("文件转移", msg, 100, style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
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

#获得路径下列表中的所有(或指定)文件目录的大小
def getDirSize(dirpath, nlist=None):
    size = 0
    if nlist == None:
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

#转移单个文件夹到新的目录下
def moveFtoF(oldpath, newpath, override=False):
    if override:
        modname = os.path.split(oldpath)[1]
        shutil.rmtree(os.path.join(newpath, modname))
        shutil.move(oldpath, newpath)
    else:
        shutil.move(oldpath, newpath)

#single Folder thread move
def SFthreadMove(oldpath, newpath):
    newflist = enumFolder(newpath)
    newalist = os.listdir(newpath)
    modname = os.path.split(oldpath)[1]
    if modname in newflist:
        #重名提示是否覆盖
        dlg = wx.MessageDialog(None, u"检测到有相同文件，是否覆盖？", u"警告", style = wx.YES_NO | wx.YES_DEFAULT | wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_YES:
            p = multiprocessing.Process(target=moveFtoF, args=(oldpath, newpath, True))
            p.start()
            moveDialog(oldpath)
    elif modname in newalist:
        p = multiprocessing.Process(target=moveFtoF, args=(oldpath, newpath, True))
        p.start()
        moveDialog(oldpath)
    else:
        p = multiprocessing.Process(target=moveFtoF, args=(oldpath, newpath))
        p.start()
        moveDialog(oldpath)
    return p

def getDirSizeFromList(pathlist):
    size = 0
    for each in pathlist:
        size += getDirSize(each)
    return size

def rmDialog(pathlist):
    allsize = getDirSizeFromList(pathlist)
    #文件大于50M则显示dialog进度条
    if allsize > 52428800 :
        msg = 'Loading...\n文件删除中，请稍等...'
        dialog = wx.ProgressDialog("文件删除", msg,100,style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        alive = True
        percent = 0
        while alive and percent < 100:
            leftsize = getDirSizeFromList(pathlist)
            percent = 100 - ((allsize-leftsize)/allsize)*100
            if percent == 100:
                msg = 'Mods删除完成！'
            #wx.Sleep(0.3)
            alive = dialog.Update(percent, newmsg=msg)
        dialog.Destroy()

def threadRMtree(pathlist):
    p = []
    newpathlist = []
    for each in pathlist:
        try:
            p.append(multiprocessing.Process(target=shutil.rmtree, args=(each,)))
            p[-1].start()
            newpathlist.append(each)
        except FileNotFoundError:
            pass
    rmDialog(newpathlist)
    return p

def passWhenAllDone(plist):
    while True:
        i =  0
        for each in plist:
            if not each.is_alive():
                i += 1
        if i == len(plist):
            return True

    
