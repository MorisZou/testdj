import pymysql.cursors
import cx_Oracle


class Connect():

   def __init__(self,host,sqltext1):
        
        self.sqltext1=sqltext1
        self.host=host
        self.user='root'
        self.password='root'
        self.db='db1'
        self.charset= charset='utf8mb4'
        self.cursorclass=pymysql.cursors.DictCursor

   def connectexec(self):
      
     if self.host=='192.168.56.118':

         mysqlconnect =pymysql.connect(host=self.host,
                             user=self.user,
                             password=self.password,
                             db=self.db,
                             charset=self.charset,
                              cursorclass=self.cursorclass)
         result_cur01=mysqlconnect.cursor()
         result_cur01.execute(self.sqltext1)
         resultall=result_cur01.fetchall()

         result_count=[]
         for row in resultall:
           result_count.append(row.values())
         return result_count 

     if self.host=='172.30.16.136':
        
           oraconnect=cx_Oracle.connect(
                             user='queryuser',
                             password='queryuser',
                             dsn='172.30.16.136/orclpdb')
           oracursor=oraconnect.cursor()
           try:
             result_count=oracursor.execute(self.sqltext1).fetchall()
           except cx_Oracle.DatabaseError,e:
               return str(e)
           else:
              return  result_count
              





