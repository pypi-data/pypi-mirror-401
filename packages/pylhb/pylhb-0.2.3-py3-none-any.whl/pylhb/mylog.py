"""
模块：mylog
作者：李生
"""
import os
from datetime import datetime
import inspect

# 日志处理类
class MyLog:
    # 初始化
    # 注意：保留天数（retainDays）必须在toLogFolder=True时才有效
    def __init__(self, logType="Log", logFile='',toLogFolder=True,retainDays=30):
        self.logType = logType
        if len(self.logType)==0:
            self.logType = "Log"
        self.logFile= logFile
        if len(self.logFile) == 0:
            self.logFile=self.getTodayFileName()
        self.toLogFolder = toLogFolder
        self.retainDays = retainDays
        if toLogFolder:
            if not os.path.exists("Logs"):
                os.makedirs("Logs")
            
        
    # 获取今天的日志文件名
    def getTodayFileName(self):
        if self.toLogFolder:
            return os.path.join("Logs", self.logType + "-" + datetime.now().strftime("%Y-%m-%d") + ".txt")
        else:
            return self.logType + "-" + datetime.now().strftime("%Y-%m-%d") + ".txt"
        
    # 删除过期日志
    def deleteExpiredLogs(self):
        if self.toLogFolder:
            logDir = "Logs"
            if os.path.exists(logDir):
                for filename in os.listdir(logDir):
                    filePath = os.path.join(logDir, filename)
                    if os.path.isfile(filePath):
                        fileDate = datetime.strptime(filename.split('-')[1].split('.')[0], "%Y-%m-%d")
                        if (datetime.now() - fileDate).days > self.retainDays:
                            os.remove(filePath)
        
    # 添加日志
    def add(self,log):
        callFrame = inspect.currentframe().f_back
        callInfo = inspect.getframeinfo(callFrame)
        with open(self.logFile, 'a', encoding='utf-8') as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " => " + f"{callInfo.filename} > {callInfo.function} > {callInfo.lineno}行" + "：" + log + "\n")
        