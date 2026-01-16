"""
模块：myjson
作者：李生
"""
import json

# JSON读写
class MyJSON:
    # 构造函数
    def __init__(self,jsonFile="config.json") -> None:
        self.jsonFile=jsonFile
        
    # 获取Key
    def getKey(self,key):
        with open(self.jsonFile,'r', encoding="utf-8") as f:
            configs=json.load(f)
        return configs[key]
    
    # 设置Key
    def setKey(self,key,value):
        # 读取
        with open(self.jsonFile,'r', encoding="utf-8") as f:
            configs=json.load(f)
        # 设置参数
        configs[key]=value
        # 保存
        with open(self.jsonFile, 'w', encoding="utf-8") as f:
            json.dump(configs, f)
