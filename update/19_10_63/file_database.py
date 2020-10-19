import sqlite3
from sqlite3 import Error

class File_database(object):
    def __init__(self):
        self.conn = sqlite3.connect("file database management.db")
        self.cur = self.conn.cursor()
        self.username = ""
        self.conn.execute("""CREATE TABLE IF NOT EXISTS users(
                            username text PRINARY KEY,
                            password text NOT NULL);""")
    def register_account(self,username,password):
        self.cur.execute("""INSERT INTO users (username,password) VALUES (?,?)""",(username,password))
        self.conn.commit()
        self.add_user_table(username)
        print("Register Complete...")
    def add_user_table(self,username):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS {}(
                            title text ,
                            author text NOT NULL,
                            filename text NOT NULL,
                            data text NOT NULL,
                            type_from text );""".format(username))
    def add_item(self,title,author,filename,data,type_from):
        try :
            sql_command = """INSERT INTO {}(title,author,filename,data,type_from) VALUES (?,?,?,?,?)""".format(self.username)
            self.cur.execute(sql_command,(title,author,filename,data,type_from,))
            self.conn.commit()
        except Error as e:
            print(e)

    def search_name(self,user):
        try :
            sql_command = """SELECT * FROM users WHERE username = ?"""
            self.cur.execute(sql,(user,))
        except :
            return None
        else:
            try :
                user = self.cur.fetchall()[0][0]
            except :
                return None
            else:
                return user
    def get_item(self,type_widget,file_name_search = None):
        try:
            sql_command = """SELECT * FROM {} WHERE type_from = ?""".format(self.username)
            self.cur.execute(sql_command,(type_widget,))
        except Error as e :
            print(e)
        else :
            data = []
            for item in self.cur.fetchall() :
                if file_name_search != None :
                    if item[2].find(file_name_search) != -1 :
                        data.append(item)
                else :
                    data.append(item)
            return data
    def login(self,user,password):
        try :
            self.cur.execute("""SELECT * FROM users WHERE username = ? AND password = ?""",(user,password,))
        except :
            print("The Username is invalid")
        else :
            try :
                self.username = self.cur.fetchall()[0][0]
            except IndexError :
                return None
            else:
                print('Login complete...')
                return self.username

    def logout(self):
        self.username = ""
        
    def check_all_id(self):
        self.cur.execute("""SELECT * FROM users""")
        row = self.cur.fetchall()
        for item in row :
            print(item)
    def check_all_item(self):
        sql_command = """SELECT * FROM {}""".format(self.username)
        self.cur.execute(sql_command)
        row = self.cur.fetchall()
        for item in row :
            print(item)
    def del_all_table(self):
        self.cur.execute("""SELECT * FROM users""")
        row = self.cur.fetchall()
        for item in row :
            sql_command = '''DROP TABLE {}'''.format(item[0])
            self.conn.execute(sql_command)
        self.conn.execute('''DROP TABLE users''')

    def send_item(item):
        owner = item["Author : "]
        receiver = item["User to receive : "]
        title = item["Title : "]
        type_send = item["Send to :"]
        fileName = item["File name : "]
        data = item["File : "] # ต้องอ่านไฟล์ก่อนค่อยใส่ไปในตัวแปร data นี่เป็นเพียงการทดลอง
        if type_send == "send_public" :
            self.add_item(title,owner,fileName,data,'send')
            try :
                self.cur.execute("""SELECT * FROM users""")
                row = cur.fetchall()
            except :
                pass
            else:
                for item in row :
                    self.username = item[0]
                    if self.username != owner :
                        self.add_item(title,owner,fileName,data,'public')
                self.username = owner
        else:
            self.add_item(title,owner,fileName,data,'send')
            self.username = self.search_name(receiver)
            if self.username != None :
                self.add_item(title,owner,fileName,data,'private')
            self.username = owner

'''def test():
    a = File_database()
    a.register_account('aa','bb')
    a.login('aa','bb')
    a.check_all_id()
    a.add_item('a','s','d','f','g')
    a.check_all_item()
    print(a.get_item('g','d'))
    a.del_all_table()
    
test()'''
def test2():
    b = File_database()
    b.check_all_id()
