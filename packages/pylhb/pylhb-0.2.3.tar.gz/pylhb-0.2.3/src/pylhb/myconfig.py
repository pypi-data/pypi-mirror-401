"""
模块：myconfig
作者：李生
"""
import configparser
import os

class MyConfig:
    def __init__(self, configFile="config.ini"):
        self.configFile = configFile
        if not os.path.exists(self.configFile):
            with open(self.configFile, 'w', encoding='gb2312') as f:
                f.write("[main]\n")
        self.cf = configparser.ConfigParser()
        self.cf.read(self.configFile, encoding='gb2312')

    # 获取节点值
    def get(self, section, option,defaultValue=""):
        if self.cf.has_section(section) and self.cf.has_option(section, option):
            return self.cf.get(section, option)
        return defaultValue

    # 设置节点值
    def set(self, section, option, value):
        if self.cf.has_section(section) is False:
            self.cf.add_section(section)
        self.cf.set(section, option, value)
        with open(self.configFile, 'w', encoding='gb2312') as f:
            self.cf.write(f)
            
    # 删除节点
    def remove(self, section, option):
        self.cf.remove_option(section, option)
        with open(self.configFile, 'w', encoding='gb2312') as f:
            self.cf.write(f)
            
    