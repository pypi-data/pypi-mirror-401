## 🌺myodbc

通过ODBC访问Microsoft SQL Server。

注意：

> ODBC Driver 17 for SQL Server下载：  
> https://learn.microsoft.com/zh-cn/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16  
> 注意，如果是ODBC Driver 18 for SQL Server，那实例化时记得传driver.

使用示例：

```
if __name__ == "__main__":
    server="127.0.0.1"
    user="sa"
    password="fpsoft@123"
    database="MyCustomer"
    # 实例化
    #mssql=MSSQL(server=server,database=database)
    mssql=MSSQL(server=server,user=user,password=password,database=database)
    # 连接数据库
    (successed,msg)=mssql.connect()
    # print(successed)
    # print(msg)
    print("数据库连接是否成功：")
    print(mssql.Connected)

    # Demo1：查询数据
    sql="SELECT TOP 2 P_CusName,P_Tel FROM Dt_Customers WITH(NOLOCK)"
    print("🌸Demot1：获取客户：")
    humans=mssql.get(sql)
    print(humans)

    # Demo2：执行无参存储过程
    # (successed,msg) = mssql.execProc("Usp_TestNoArgs")
    # print("🌸Demot2：执行无参存储过程(Usp_TestNoArgs)：")
    # print(successed,msg)

    # Demo3：执行带参存储过程
    # (successed,msg) = mssql.execProc("Usp_TestWithArgs",(99,"1号机"))
    # print("🌸Demot3：执行带参存储过程(Usp_TestWithArgs)：")
    # print(successed,msg)

    # Demo4：执行存储过程并返回数据
    # (successed,msg,datas) = mssql.execProcGet("Usp_Test",("",))
    # print("🌸Demot4：执行存储过程并返回数据(Usp_Test)：")
    # print(successed,msg,datas)

    # Demo5：Insert
    # user1 = {"P_UserName": "张三", "P_Age": 25, "P_Email": "Zhang3@example.com"}
    # user2 = {"P_UserName": "李四", "P_Age": 20, "P_Email": "Li4@example.com"}
    # user3 = {"P_UserName": "王五", "P_Age": 18, "P_Email": "Wang5@example.com"}
    # (successed,msg)=mssql.insert("Dt_User",user1)
    # (successed,msg)=mssql.insert("Dt_User",user2)
    # (successed,msg)=mssql.insert("Dt_User",user3)
    # print(successed,msg)

    # Demo6：Update
    # updateData = {"P_Age": 31,"P_Email":"Zhang3@QQ.com"}
    # (successed,msg)=mssql.update("Dt_User", updateData, "P_UserName = ?",('张三',))
    # print(successed,msg)

    # Demo7：Delete
    # (successed,msg)=mssql.delete("Dt_User", "P_UserName = ?", ("王五",))
    # print(successed,msg)

    # Demo8：Select
    # cols=("P_UserName","P_Age")
    # cols=None
    # (successed,msg,data)=mssql.select("Dt_User",cols,"P_UserName = ?",("张三",))
    # print(successed,msg,data)

    # 提交事务
    mssql.commit()
    # 关闭
    mssql.close()
```
