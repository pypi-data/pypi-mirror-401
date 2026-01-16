'''
模块：pyodbc封装
作者：李生
注意：
ODBC Driver 17 for SQL Server下载：
https://learn.microsoft.com/zh-cn/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16
注意，如果是ODBC Driver 18 for SQL Server，那实例化时记得传driver.
'''
import pyodbc

class MSSQL:
    def __init__(self,*,server=None,user=None,password=None,database=None,port=1433,timeout=0,autoCommit=False,trusted=False,driver="ODBC Driver 17 for SQL Server") -> None:
        self.server=server
        self.user=user
        self.password=password
        self.database=database
        self.port=port
        self.timeout=timeout
        self.autoCommit=autoCommit
        self.trusted=trusted
        self.driver=driver
        self.conn=None
        self.cursor=None
        
    def getConnectString(self) -> str:
            conn_str = f"DRIVER={{{self.driver}}};SERVER={self.server},{self.port};DATABASE={self.database};"
            
            if self.trusted:
                conn_str += "Trusted_Connection=yes;"
            else:
                if self.user and self.password:
                    conn_str += f"UID={self.user};PWD={self.password};"
                if self.timeout>0:
                    conn_str += f"Connection Timeout={self.timeout};"
            
            return conn_str
        
    def connect(self) -> tuple[bool,str]:
        try:
            connectString = self.getConnectString()
            self.conn = pyodbc.connect(connectString)
            self.cursor=self.conn.cursor()
            return True,"OK"
        except Exception as e:
            self.conn=None
            self.cursor=None
            return False,str(e)
            
    # 获取连接状态
    @property
    def Connected(self):
        return self.conn is not None
        
    # 设置自动提交
    def setAutoCommit(self,autoCommit):
        if not self.conn:
            return False,"未连接数据库。"
        try:
            self.conn.autocommit=autoCommit
            return True
        except Exception as e:
            return False
            
    # 获取是否自动提交
    @property
    def IsAutoCommit(self):
        return self.conn.autocommit
        
    # 插入记录
    def insert(self, tableName: str, data: dict):
        if not self.conn:
            return False,"未连接数据库。"
        try:
            columns = ", ".join(data.keys())
            values = tuple(data.values())
            sql = f"INSERT INTO {tableName} ({columns}) VALUES {values}"
            self.cursor.execute(sql)
            return (True,"OK")
        except Exception as e:
            return (False,str(e))
            
    # 修改记录
    def update(self, table_name: str, data: dict, where: str, params: tuple[any]):
        if not self.conn:
            return False,"未连接数据库。"
        try:
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            values = tuple(data.values()) + params
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
            self.cursor.execute(sql, values)
            return (True,"OK")
        except Exception as e:
            return (False,str(e))
        
    # 删除记录
    def delete(self, table_name: str, where: str, params: tuple[any]):
        if not self.conn:
            return False,"未连接数据库。"
        try:
            sql = f"DELETE FROM {table_name} WHERE {where}"
            self.cursor.execute(sql, params)
            return (True,"OK")
        except Exception as e:
            return (False,str(e))
            
    # 查询数据
    def select(self, table_name, columns: tuple[str] = None, where=None, params: tuple[any]=None,toDict=True):
        if not self.conn:
            return False,"未连接数据库。",None
        try:
            cols = "*" if columns is None else ", ".join(columns)
            sql = f"SELECT {cols} FROM {table_name}"
            if where:
                sql += f" WHERE {where}"
            print(sql)
            if where and params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            if toDict:
                # 获取列名
                columns = [column[0] for column in self.cursor.description]
                # 转换为字典列表
                data = []
                for row in self.cursor.fetchall():
                    data.append(dict(zip(columns, row)))
                return True,"OK",data
            else:
                data = self.cursor.fetchall()
                return True,"OK",data
        except Exception as e:
            return False,str(e),None
            
    # 查询数据
    def get(self,sql,toDict=True):
        if not self.conn:
            return None
        try:
            self.cursor.execute(sql)
            if toDict:
                # 获取列名
                columns = [column[0] for column in self.cursor.description]
                # 转换为字典列表
                results = []
                for row in self.cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                return self.cursor.fetchall()
        except:
            return None

    # 执行SQL
    def exec(self,sql):
        if not self.conn:
            return False,"未连接数据库。"
        try:
            self.cursor.execute(sql)
            return (True,"OK")
        except Exception as e:
            return (False,str(e))

    # 执行存储过程
    def execProc(self,procName,params: tuple[any] = None):
        if not self.conn:
            return (False,"未连接数据库。")
        try:
            if params:
                placeholders = ', '.join(['?' for _ in params])
                sql = f"EXEC {procName} {placeholders}"
                self.cursor.execute(sql, params)
            else:
                sql = f"EXEC {procName}"
                self.cursor.execute(sql)
            return (True,"OK")
        except Exception as e:
            return (False,str(e))

    # 执行存储过程并返回数据
    def execProcGet(self,procName,params: list[any] = None):
        if not self.conn:
            return (False,"未连接数据库。",None)
        try:
            if params:
                placeholders = ', '.join(['?' for _ in params])
                sql = f"EXEC {procName} {placeholders}"
                self.cursor.execute(sql, params)
            else:
                sql = f"EXEC {procName}"
                self.cursor.execute(sql)
                
            datas = []
            if self.cursor.description:
                columns = [desc[0] for desc in self.cursor.description]
                for row in self.cursor.fetchall():
                    datas.append(dict(zip(columns, row)))
                    
            return (True,"OK",datas)
        except Exception as e:
            return (False,str(e),None)

    # 提交事务
    def commit(self):
        if not self.conn:
            return
        if self.conn.autocommit==True:
            return
        self.conn.commit()

    # 回滚事务
    def rollback(self):
        if not self.conn:
            return
        self.conn.rollback()

    # 关闭连接
    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor=None
        if self.conn:
            self.conn.close()
            self.conn=None
