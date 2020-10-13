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
        self.cur.execute("""INSERT INTO users (username,password) VALUE (?,?)""",(username,password))
        self.add_user_table(username)
    def add_user_table(self,username):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS {}(
                            title text NOT NULL,
                            author text NOT NULL,
                            filename text NOT NULL,
                            data text NOT NULL,
                            type_from text NOT NULL,
                            type_file text NOT NULL);""".format(username))
    def add_item(self,title,author,filename,data,type_from,type_file):
        self.cur.execute(("""INSERT INTO {}(title,author,filename,data,type_from,type_file) VALUE (?,?,?,?,?,?)"""
                            ,(title,author,filename,data,type_from,type_file)).format(self.username))
    def get_item(self,type_widget,file_name_search = None):
        try:
            self.cur.excute("""SELECT * FROM {} WHERE type_from = {}""".format(self.username,type_widget))
        except Error :
            pass
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
            self.cur.execute("""SELECT * FROM users WHERE username = {} AND password = {}""".format(user,password))
        except Error :
            pass
        else :
            self.username = user
            return user