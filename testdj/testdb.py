from connect import Connect


conn1=Connect()
cur=conn1.connectdb()
cur01=cur.cursor()
cur01.execute("update db1.t2 set a=a+1")
cur01.execute("commit")
