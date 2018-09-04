# -*- coding:utf-8 -*-

import re

###获取文件内容
def readFile(filePath, mode='r', by = 'lines'):
    with open(filePath,mode) as f:
        if(by == 'lines'):
            return f.readlines()
        elif(by == 'all'):
            return f.read()
        else:
            print('未选择读取方法！')
        
###按行匹配并提取（要提取的）文件数据      
def strRegx(paramStr):
    pattern = r'\d{8}\s+\d{6}\s+(\w{8})\s+\d{8}\s+(\d{1})\s+(\w+).*'
    #pattern = r'(?:[a-fA-F\d]+?\s+?){2}([a-fA-F\d]+?)\s+?[a-fA-F\d]+?\s+?(\d+?)\s+?([^.*@%%]\w+?)'
    matchObj = re.match(pattern,paramStr,re.I)      ###匹配paramStr
    if not matchObj is None:                        ###格式化字符串输出
        formatStr = ''' 
  /begin MEASUREMENT {0}
   "" 
   {1} 
   ident
   0.1 
   100
   0 
   20
   ECU_ADDRESS {2}
  /end MEASUREMENT
   '''
        if(matchObj.group(2) =='1'):
            g2 = 'SBYTE'
        elif(matchObj.group(2) =='2'):
            g2 = 'SWORD'
        elif(matchObj.group(2) =='4'):
            g2 = 'SLONG'
        else:
            g2 = 'FLOAT32_IEEE'
        #print((matchObj.group(1),g2,matchObj.group(3)))
        outputStr = formatStr.format(matchObj.group(1),g2,matchObj.group(3))
        #print(outputStr)
        return outputStr
    else:
        return None
    
###按块匹配并提取（要写入的）文件数据
def blockRegx(blockStr):
    pattern = r'\s+/begin MEASUREMENT.*/end MEASUREMENT'
    matchObj = re.search(pattern,blockStr,re.S)             ##使 . 匹配包括换行在内的所有字符
    if(matchObj):
        return matchObj.group()              

if __name__ == '__main__':
    lines = readFile('INTC_HW_VLE-flash.MAP','r','lines')   ##提取数据文件行内容列表
    data = readFile('MPC5604_BMS2.a2l','r','all')           ##提取写入文件的所有内容
    replA = blockRegx(data)
    replB = ''
    for line in lines[975:1081]:                            ##提取数据文件976-1081行的内容
        out = strRegx(line.lstrip())                        ##去除行内容前的空格进行匹配，否则修改正则
        if(out):
            replB += out   
    if(replA and replB):
        output = data.replace(replA,replB)                  ##replB替换data里的replA
        with open('MPC5604_BMS2_副本.a2l','w+') as f:
            f.write(output)
            print("Success!")
    else:
        print("repl数据不存在！")
    
    







        
