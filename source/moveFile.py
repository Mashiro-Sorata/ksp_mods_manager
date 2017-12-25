import shutil
import os
import multiprocessing
import time
import wx

#复制某个文件夹下所有文件(包括文件夹)
def moveFinF(oldpath, newpath):
    flist = os.listdir(oldpath)
    for each in flist:
        try:
            shutil.move(os.path.join(oldpath,each),newpath)
        except shutil.Error:
            pass

def threadMoveWithDialog(oldpath, newpath):
    p = multiprocessing.Process(target=moveFinF, args=(oldpath, newpath))
    p.start()
    dialog = wx.ProgressDialog("A progress box", "Time remaining",100,style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
    allsize = getDirSize(oldpath)
    alive = True
    num = 0
    if allsize:
        while alive and num < 100:
            leftsize = getDirSize(oldpath)
            num = ((allsize-leftsize)/allsize)*100
            alive = dialog.Update(num)
    dialog.Destroy()

def getModsNum(dirpath):
    flist = []
    for each in os.listdir(dirpath):
        if os.path.isdir(each):
            flist.append(each)
    

def getDirSize(dirpath):
    size = 0
    for (root,dirs,files) in os.walk(dirpath):
        for name in files:
            try:
                size += os.path.getsize(os.path.join(root, name))
            except:
                continue
    return size


if __name__ == '__main__':
    print(getDirSize(os.getcwd())/1024/1024,'M')
