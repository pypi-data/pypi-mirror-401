"""
模块：mysqlite
作者：李生
"""
import sqlite3
from typing import List, Tuple, Any, Optional

class SQLite:
    def __init__(self, dbName: str = "data.db"):
        self.dbName = dbName
        self.connection = None
        self.cursor = None
    
    # 连接数据库
    def connect(self) -> tuple[bool,str]:
        try:
            self.connection = sqlite3.connect(self.dbName)
            self.cursor = self.connection.cursor()
            return True,"OK"
        except sqlite3.Error as e:
            return False,str(e)
    
    # 创建表
    def createTable(self, tableName: str, columns: dict) -> tuple[bool,str]:
        if not self.connection:
            self.connect()
        cols = ", ".join([f"{name} {defn}" for name, defn in columns.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {tableName} ({cols})"
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return True,"OK"
        except sqlite3.Error as e:
            return False,str(e)
    
    # 插入记录
    def insert(self, tableName: str, data: dict) -> tuple[bool,Optional[int]]:
        if not self.connection:
            self.connect()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())
        sql = f"INSERT INTO {tableName} ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True,self.cursor.lastrowid
        except sqlite3.Error as e:
            return False,None
    
    # 查询数据
    def select(self, tableName: str, columns: List[str] = None, where: str = None, params: Tuple[Any] = None) -> tuple[bool,List[Tuple]]:
        if not self.connection:
            self.connect()
        cols = "*" if columns is None else ", ".join(columns)
        sql = f"SELECT {cols} FROM {tableName}"
        if where:
            sql += f" WHERE {where}"
        try:
            if where and params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return True,results
        except sqlite3.Error as e:
            return False,[]
    
    # 更新数据
    def update(self, tableName: str, data: dict, where: str, params: Tuple[Any]) -> tuple[bool,str]:
        if not self.connection:
            self.connect()
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values()) + params
        sql = f"UPDATE {tableName} SET {set_clause} WHERE {where}"
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True,"OK"
        except sqlite3.Error as e:
            return False,str(e)
    
    # 删除数据
    def delete(self, tableName: str, where: str, params: Tuple[Any]) -> tuple[bool,str]:
        if not self.connection:
            self.connect()
        sql = f"DELETE FROM {tableName} WHERE {where}"
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            return True,"OK"
        except sqlite3.Error as e:
            return False,str(e)
    
    # 关闭连接
    def close(self) -> None:
        if self.cursor:
            self.cursor.close()
            self.cursor=None
        if self.connection:
            self.connection.close()
            self.connect=None
