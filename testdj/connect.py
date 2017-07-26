import pymysql.cursors
import cx_Oracle
import logging

class Connect():

   def __init__(self,host,sqltext1):
        
        self.sqltext1=sqltext1
        self.host=host
        self.user='root'
        self.password='root'
        self.db='db1'
        self.charset= charset='utf8mb4'
        self.cursorclass=pymysql.cursors.DictCursor

   def connectexec(self,page_id=1):
     logger=logging.getLogger('testdj')
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
             result_desc_init=oracursor.execute('select * from ('+self.sqltext1+') where 1=0').description
             rec_count=oracursor.execute(self.sqltext1).fetchall()            
           except cx_Oracle.DatabaseError,e:
             result_desc=''
             page_counts=''  
             return (result_desc,str(e),page_counts)
           else:
             page_counts=[]
             result_desc=[]
             col_str=''
             for i in range((len(rec_count)/300)+1):
                page_counts.append(i+1)

             for result_desc_for in result_desc_init:
                 result_desc.append(result_desc_for[0])
                 col_str=col_str+result_desc_for[0]+','

             #sqltext='select ' +col_str+' rid from '+ (('select '+col_str+'rownum rid from ('+self.sqltext1+'))  'where rid>'+(str((page_id-1)*300))+' and rid<='+(str((page_id)*300))
             sqltext='select '+ col_str+'RID from ('+'select '+col_str+'rownum RID  from ('+self.sqltext1+')) where RID>'+(str((int(page_id)-1)*300))+' and RID<='+(str((int(page_id))*300))
             logger.info(sqltext)
             result_count=oracursor.execute(sqltext).fetchall()
             result_desc.append('RID')
             return (result_desc,result_count,page_counts)
              





