import websockets
import asyncio
import sys
import json
from class_file import *

async def main():
    ip = "localhost" # Enter your server ip.
    port = "8000" # Enter your server port.
    authorize = False
    async with websockets.connect(f"ws://{ip}:{port}") as conn:
        while True:
            if authorize:
                comm = input("[Export, Browse, Download] : ")
                
                if comm == "Export":
                    await sendfile(conn, username)
                    
                
                elif comm == "Browse":
                    await browse(conn, username)                    
                
                elif comm == "Download":
                    while True:
                        comm = input("[Public, Inbox] : ")
                        if comm == "Public" or comm == "Inbox":
                            await downloadfile(conn, comm, username)
                        else:
                            continue
                        break

                else:
                    continue

            else:
                comm = input("[Login, Register] : ")
                
                if comm == "Register":
                    await register(conn)
                
                elif comm == "Login":
                    authorize, username = await login(conn)
                
                else:
                    continue

def test_open():
    file_path = input("Enter your file path : ")
    try:
        f = open(r"{}".format(file_path), "r")
        return file_path
    except:
        print("Can't find a file.")
        return test_open()

async def find_user(conn):
    dest_user = input("Who you want to send to (Username) : ")
    await conn.send("find_user")
    await asyncio.sleep(1)
    await conn.send(dest_user)
    await asyncio.sleep(1)
    confirm = await conn.recv()
    if confirm:
        return dest_user
    else:
        await find_user(conn)

async def find_sendmode(conn):
    file_comm = input("Public or Private : ")
    if file_comm == "Private":
        dest_user = await find_user(conn)
        return "send_direct", dest_user
    elif file_comm == "Public":
        return "send_public", "foo"
    else:
        await find_sendmode(conn)

def find_browse():
    browse = input("[Inbox, Public, Sendhistory] : ")
    if browse == "Inbox":
        return "browse_inbox"
    elif browse == "Public":
        return "browse_public"                        
    elif browse == "Sendhistory":
        return "browse_history"
    else:
        find_browse()

def custom_path(filepath):
    filename_index = -1
    while filepath[filename_index] != "\\":
        filename_index -= 1
    filename = filepath[filename_index+1:]
    fileextension_index = -1
    while filepath[fileextension_index] != ".":
        fileextension_index -= 1
    fileextension = filepath[fileextension_index:]
    return filename, fileextension

async def checksenderfile(conn, filepath):
    file_size = measure(filepath)
    await conn.send("checkfile")
    await asyncio.sleep(1)
    await conn.send(file_size)
    await asyncio.sleep(1)
    confirm_status = await conn.recv()
    if confirm_status == "complete":
        print("File completly send")
    else:
        print("File incompletely send")

async def read(conn, filepath):
    f = open(r"{}".format(filepath), 'r')
    for r in f:
            print(r)
            jsonr = json.dumps(r)
            await conn.send(jsonr)
            await asyncio.sleep(1)
    f.close()
    await conn.send(json.dumps("SendingEnd"))

def measure(filepath):
    f = open(r"{}".format(filepath), 'r')
    line_size = []
    for line in f:
        size = len(line)
        line_size.append(size)
    f.close()
    line_size_json = json.dumps(line_size)
    return line_size_json

def checkregister(username, password):
    allowchar = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    leastlength = 8
    length_error = "Your username and password must have at least 8 characters."
    char_error = "Your username and password must contain only alphabets and numbers."
    if len(username) >= leastlength and len(password) >= leastlength:
        for char in username:
            if char in allowchar:
                continue
            else:
                return False, char_error

        for char in password:
            if char in allowchar:
                continue
            else:
                return False, char_error

        return True, ""
    else:
        return False, length_error

async def register(conn):    
    register_username = input("Username : ")
    register_password = input("Password : ")
    checkregis_status, regis_error = checkregister(register_username, register_password)
    if checkregis_status == True:
        await asyncio.sleep(1)
        await conn.send("register")

        await conn.send(register_username)
        await asyncio.sleep(1)

        await conn.send(register_password)
        await asyncio.sleep(1)

        confirmregis = await conn.recv()
        if confirmregis == "True":
            print("Success to register.")
        else:
            print("Your username is already taken. Try use a new one.")
            await register(conn)
    else:
        return print(regis_error)

async def login(conn):    
    login_username = input("Username : ")
    login_password = input("Password : ")
    
    await conn.send("login")
    await asyncio.sleep(1)
    await conn.send(login_username)
    await asyncio.sleep(1)
    await conn.send(login_password)
    await asyncio.sleep(1)           

    login_status = await conn.recv()
    
    if login_status == "True":
        return True, login_username
    else:
        print("Error : Your username or password are wrong.")
        while True:
            recur = input("Do you want to try login again? [Yes, No] : ")
            if recur == "Yes":
                authorize, username = await login(conn)
                return authorize, username
                break
            elif recur == "No":
                break
            else:
                continue
        return False, None

async def sendfile(conn, username):
    file_path = test_open()
    title = input("Write your title : ")
    author = username
    filename, fileextension = custom_path(file_path)
    send_mode, dest_user = await find_sendmode(conn)
    
    file_data = [title, author, dest_user, filename, fileextension]
    file_json = json.dumps(file_data)
    
    await conn.send(send_mode)
    await asyncio.sleep(1)
    await conn.send(username)
    await asyncio.sleep(1)
    await conn.send(file_json)
    await asyncio.sleep(1)
    await read(conn, file_path)
    await asyncio.sleep(1)

async def browse(conn, username):
    browse_comm = find_browse()
    await conn.send(browse_comm)
    
    await asyncio.sleep(1)
    await conn.send(username)
    
    await asyncio.sleep(1)                    
    json_inbox_list = await conn.recv()
    inbox_list = json.loads(json_inbox_list)
    if inbox_list == []:
        print("Empty")
    else:
        print("[Title, Author, Filename, Type_form]")
        for line in inbox_list:
            print(line)

async def downloadfile(conn, comm, username):
    await conn.send("download")
    await asyncio.sleep(1)

    await conn.send(username)
    await asyncio.sleep(1)

    await conn.send(comm)
    await asyncio.sleep(1)
    
    json_filenamelist = await conn.recv()
    filenamelist = json.loads(json_filenamelist)
    print(filenamelist)
    
    while True:
        targetfile = input("Choose a file to download : ")
        if targetfile in filenamelist:
            await conn.send(targetfile)
            break
        else:
            continue
    
    await write(conn, targetfile)

async def write(conn, filename):
    global default
    f = open(r"{}{}".format(default, filename), 'w')
    json_line = await conn.recv()
    line = json.loads(json_line)
    while line != "SendingEnd":
        print(line)
        await asyncio.sleep(1)
        f.write(line)
        json_line = await conn.recv()
        line = json.loads(json_line)
    f.close()
    print("END")

if __name__ == "__main__":
    default = "D:\\vs_studio\\sdp_project\\file_transfer_program\\client_save\\" # Enter your path location to save a file.
    asyncio.get_event_loop().run_until_complete(main())