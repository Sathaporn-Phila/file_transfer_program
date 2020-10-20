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
        self.conn.execute("""CREATE TABLE IF NOT EXISTS public (
                            title text ,
                            author text NOT NULL,
                            filename text NOT NULL,
                            data text NOT NULL,
                            type_form text );""")
    def register_account(self,username,password):
        self.cur.execute("""INSERT INTO users (username,password) VALUES (?,?)""",(username,password))
        self.conn.commit()
        self.send_history_table(username)
        self.inbox_table(username)
        print("Register Complete...")
    def send_history_table(self,username):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS {}_send(
                            title text ,
                            author text NOT NULL,
                            filename text NOT NULL,
                            data text NOT NULL,
                            type_form text );""".format(username))
    
    def add_send_history(self,title,author,filename,data,type_form):
        try :
            sql_command = """INSERT INTO {}_send(title,author,filename,data,type_form) VALUES (?,?,?,?,?)""".format(self.username)
            self.cur.execute(sql_command,(title,author,filename,data,type_form,))
        except Error as e:
            print(e)
        else :
            self.conn.commit()
    
    def get_send_history(self,file_name_search = None):
        try:
            sql_command = """SELECT * FROM {}_send """.format(self.username)
            self.cur.execute(sql_command)
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
    
    def inbox_table(self,username):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS {}_inbox(
                            title text ,
                            author text NOT NULL,
                            filename text NOT NULL,
                            data text NOT NULL,
                            type_form text );""".format(username))

    def add_inbox(self,target,title,author,filename,data,type_form):
        try :
            sql_command = """INSERT INTO {}_inbox(title,author,filename,data,type_form) VALUES (?,?,?,?,?)""".format(target)
            self.cur.execute(sql_command,(title,author,filename,data,type_form,))
        except Error as e:
            print(e)
        else:
            self.conn.commit()
    
    def get_inbox(self,file_name_search = None):
        try:
            sql_command = """SELECT * FROM {}_inbox """.format(self.username)
            self.cur.execute(sql_command)
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
    
    def add_public(self,title,author,filename,data,type_form):
        try :
            sql_command = """INSERT INTO public(title,author,filename,data,type_form) VALUES (?,?,?,?,?)"""
            self.cur.execute(sql_command,(title,author,filename,data,type_form,))
        except Error as e:
            print(e)
        else:
            self.conn.commit()

    def get_public(self,file_name_search = None):
        try:
            sql_command = """SELECT * FROM public """
            self.cur.execute(sql_command)
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
    def search_name(self,user):
        try :
            sql_command = """SELECT * FROM users WHERE username = ?"""
            self.cur.execute(sql_command,(user,))
        except :
            return None
        else:
            try :
                user = self.cur.fetchall()[0][0]
                print(user)
            except :
                return None
            else:
                return user

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
        sql_command = """SELECT * FROM {}_send """.format(self.username)
        self.cur.execute(sql_command)
        row = self.cur.fetchall()
        for item in row :
            print(item)
    def del_all_table(self):
        self.cur.execute("""SELECT * FROM users""")
        row = self.cur.fetchall()
        for item in row :
            sql_command = '''DROP TABLE {}_send'''.format(item[0])
            sql_command2 = '''DROP TABLE {}_inbox'''.format(item[0])
            self.conn.execute(sql_command)
            self.conn.execute(sql_command2)
        self.conn.execute('''DROP TABLE public''')
        self.conn.execute('''DROP TABLE users''')

    def send_item(self,item):
        owner = item["Author : "]
        receiver = item["User to receive : "]
        title = item["Title : "]
        type_send = item["Send to : "]
        print(type_send)
        fileName = item["File name"]
        type_file = item["Type file"]
        data = item["File : "] # ต้องอ่านไฟล์ก่อนค่อยใส่ไปในตัวแปร data นี่เป็นเพียงการทดลอง
        if type_file != fileName : # error string of find method when it is not found 
            if type_send == "send_public" :
                self.add_send_history(title,owner,fileName,data,type_file)
                print(self.get_send_history())
                try :
                    self.cur.execute("""SELECT * FROM users""")
                    row = self.cur.fetchall()
                except :
                    pass
                else:
                    self.add_public(title,owner,fileName,data,type_file)
            else:
                receiver_username = self.search_name(receiver)
                print(receiver_username)
                if receiver_username != None :
                    self.add_send_history(title,owner,fileName,data,type_file)
                    self.add_inbox(receiver_username,title,owner,fileName,data,type_file)
                    print(self.get_inbox())
                self.username = owner

def test():
    a = File_database()
    a.del_all_table()
    
def test2():
    b = File_database()
    print(b.username)

def test3():
    c = File_database()
    c.check_all_id()