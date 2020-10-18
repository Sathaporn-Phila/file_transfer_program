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
        self.conn.execute("""CREATE TABLE IF NOT EXISTS public(
                            title text ,
                            author text NOT NULL,
                            filename text NOT NULL,
                            data text NOT NULL,
                            type_form text );""")
    
    def register_account(self,username,password):
        self.cur.execute("""INSERT INTO users (username,password) VALUES (?,?)""",(username,password))
        self.send_history_table(username)
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
    
    def get_send_history(self,type_widget,file_name_search = None):
        try:
            sql_command = """SELECT * FROM {}_send WHERE type_form = ?""".format(self.username)
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
    
    def get_inbox(self,type_widget,file_name_search = None):
        try:
            sql_command = """SELECT * FROM {}_inbox WHERE type_form = ?""".format(self.username)
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
    
    def add_public(self,title,author,filename,data,type_form):
        try :
            sql_command = """INSERT INTO public(title,author,filename,data,type_form) VALUES (?,?,?,?,?)"""
            self.cur.execute(sql_command,(title,author,filename,data,type_form,))
        except Error as e:
            print(e)

    def login(self,user,password):
        try :
            self.cur.execute("""SELECT * FROM users WHERE username = ? AND password = ?""",(user,password,))
        except Error :
            print("The Username is invalid")
        else :
            self.username = user
            print('Login complete...')
            return user

    def logout(self):
        self.username = ""
        
    def check_all_id(self):
        self.cur.execute("""SELECT * FROM users""")
        row = self.cur.fetchall()
        for item in row :
            print(item)
    def check_all_item(self):
        sql_command = """SELECT * FROM {}_send""".format(self.username)
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