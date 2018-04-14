
# coding: utf-8

# In[5]:

import MySQLdb
db = MySQLdb.connect(host="localhost",user="root", passwd="",db="apple", charset="utf8")
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS appleNews")

# 创建数据表SQL语句
sql = "CREATE TABLE appleNews (_ID  INT NOT NULL auto_increment primary key,         Link VARCHAR(1000),        Title VARCHAR(1000),         Content VARCHAR(1000),        View_number VARCHAR(1000),        Post_time VARCHAR(1000) )"

cursor.execute(sql)

# 关闭数据库连接
db.close()


# In[ ]:



