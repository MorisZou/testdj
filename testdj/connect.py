import pymysql.cursors

class Connect():

   def __init__(self):

        self.host='localhost'
        self.user='root'
        self.password=''
        self.db='db1'
        self.charset= charset='utf8mb4'
        self.cursorclass=pymysql.cursors.DictCursor

   def connectdb(self):
         return pymysql.connect(host=self.host,
                             user=self.user,
                             password=self.password,
                             db=self.db,
                             charset=self.charset,
                             cursorclass=self.cursorclass)

