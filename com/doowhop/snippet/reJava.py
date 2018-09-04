# -*- coding:utf-8 -*-

import re
import os

#获取文件夹下所有文件
def getFiles(fileDir, suffix):
    fileList = []
    for root, dirs, files in os.walk(fileDir): 
        #print(root) #当前目录路径
        #print(dirs) #当前路径下所有子目录 
        #print(files) #当前路径下所有非目录子文件 
        for file in files:
            (shotname,extension) = os.path.splitext(file);
            if(extension == suffix):
                fileList.append(os.path.join(root,file))  #根目录与文件名组合，形成绝对路径。           
    return fileList
    
###获取文件内容
def readFile(filePath, mode='r', by = 'lines'):
    with open(filePath,mode,encoding="utf-8") as f:
        if(by == 'lines'):
            return f.readlines()
        elif(by == 'all'):
            return f.read()
        else:
            print('未选择读取方法！')
        
#===============================================================================
# def ReadFile(filePath,encoding="utf-8"):
#     with codecs.open(filePath,"r",encoding) as f:
#         return f.read()
#  
# def WriteFile(filePath,u,encoding="utf-8"):
#     with codecs.open(filePath,"w",encoding) as f:
#         f.write(u)
#===============================================================================
         
###按块匹配并提取（要写入的）文件数据
def blockRegx(blockStr):
    pattern = r';\s+(/\*\*.*?\*/)'
    matchObj = re.search(pattern,blockStr,re.S)             ##使 . 匹配包括换行在内的所有字符
    if(matchObj):
        return matchObj.group(1)  

def strRegx(reStr):
    pattern = r'.*@Description.*(.*?)'
    matchObj = re.search(pattern,reStr,re.I)             ##使 . 匹配包括换行在内的所有字符
    if(matchObj):
        return matchObj.group()        

if __name__ == '__main__':
    path = r'E:\UNIFIED-WORKSPACES\thfund-commons\thfund-commons_trunk\common-help'
    i = 0
    for filePath in getFiles(path, '.java'):
        data = readFile(filePath, 'r', 'all')
        replA = blockRegx(data)
        if(replA is None):
            continue
        replB = strRegx(replA);
        if (replB is None):
            replB = ''
        else:
            replB = '/**\n ' + replB + '\n */'
        output = data.replace(replA,replB)  
        with open(filePath,'w+',encoding="utf-8") as f:
            print(filePath)
            f.write(output)
            i=i+1
    print(str(i)+" Success!")
    
        
