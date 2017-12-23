# folder_list.py
# -*- coding: utf-8 -*-

import os

def enumFolder(path, main=True):
    dir_list = []
    alist = os.listdir(path)
    for each in alist:
        new_path = os.path.join(path,each)
        if not main:
            if os.path.isfile(new_path):
                return True
            else:
                if enumFolder(new_path, False):
                    return True
        else:
            if not os.path.isfile(new_path):
                if enumFolder(new_path, False):
                    dir_list.append(each)
    return dir_list

def folder2data(path):
    data = {}
    tag = 'undefined'
    dlist = enumFolder(path)
    for each in dlist:
        data[each] = (os.path.join(path,each), tag)
    return data
    
    

if __name__ == '__main__':
    path = r'E:\Work\python-learn\project\ksp_mods_manager\prj\test'
    data = folder2data(path)
    print(data)
