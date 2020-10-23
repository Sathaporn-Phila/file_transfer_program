import websockets
import asyncio
import sys
import json
from class_file import *

async def main():
    async with websockets.connect("ws://localhost:8000") as conn:
        while True:
            comm = input("Enter your command : [Register, Login, Send a file, Browse]\n")
            if comm == "Register":
                await asyncio.sleep(1)
                await conn.send("register")
                register_username = str(input("Username : "))
                await asyncio.sleep(1)
                await conn.send(register_username)
                print("sending username")
                register_password = str(input("Password : "))
                await asyncio.sleep(1)
                await conn.send(register_password)
                print("sending password")

            elif comm == "Login":
                check_login = True
                while check_login:
                    await asyncio.sleep(1)
                    await conn.send("login")
                    login_username = input("Username : ")
                    await asyncio.sleep(1)
                    await conn.send(login_username)
                    login_password = input("Password : ")
                    await asyncio.sleep(1)
                    await conn.send(login_password)
                    await asyncio.sleep(1)
                    login_status = await conn.recv()
                    if login_status == "pass":
                        check_login = not check_login
                username = login_username

            elif comm == "Send a file":
                file_path = test_open()
                title = input("Write your title : ")
                author = username
                filename, fileextension = custom_path(file_path)
                send_mode, dest_user = await find_sendmode(conn)
                file_data = [title, author, dest_user, filename, fileextension]
                file_json = json.dumps(file_data)
                await conn.send(send_mode)
                await asyncio.sleep(1)
                await conn.send(file_json)
                await asyncio.sleep(1)
                await send(conn, file_path)
                await asyncio.sleep(1)
                #await checksenderfile(filepath)

            elif comm == "Browse":
                browse_comm = find_browse()
                await asyncio.sleep(1)
                await conn.send(browse_comm)
                await asyncio.sleep(1)
                inbox_list = await conn.recv()
                for line in inbox_list:
                    print(line)

            else:
                await conn.send(comm)
                # rawlist = ["boom","nui"]
                # jsonlist = json.dumps(rawlist)
                # await asyncio.sleep(1)
                # await conn.send(jsonlist)
                # msg = input("msg : ")
                # await conn.send(msg)
                # echo1 = await conn.recv()
                # print(echo1)
                # echo2 = await conn.recv()
                # print(echo2)
                #print("Command not in the list.")
                # continue

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
    find = await conn.send("find_user")
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
        return "send_public", ""
    else:
        await find_sendmode(conn)

def find_browse():
    browse = input("Choose what to browse : [inbox, public, sendhistory]\n")
    if browse == "inbox":
        return "browse_inbox"
    elif browse == "public":
        return "browse_public"                        
    elif browse == "sendhistory":
        return "browse_history"
    else:
        return find_browse()

def custom_path(filepath):
    filename_index = -1
    while filepath[filename_index] != "\\":
        filename_index -= 1
    filename = filepath[filename_index+1:]
    fileextension_index = -1
    while filepath[fileextension_index] != ".":
        fileextension_index -= 1
    fileextension = filepath[fileextension_index:]
    print(filename, fileextension)
    return filename, fileextension

async def checksenderfile(conn, filepath):
    file_size = check(filepath)
    await conn.send("checkfile")
    await asyncio.sleep(1)
    await conn.send(file_size)
    await asyncio.sleep(1)
    confirm_status = await conn.recv()
    if confirm_status == "complete":
        print("File completly send")
    else:
        print("File incompletely send")

async def send(conn, filepath):
    f = open(r"{}".format(filepath), 'r')
    r = f.read()
    while r:
        jsonr = json.dumps(r)
        await conn.send(jsonr)
        await asyncio.sleep(1)
        r = f.read()
    f.close()

def check(filepath):
    f = open(r"{}".format(filepath), 'r')
    line_size = []
    for line in f:
        size = len(line)
        line_size.append(size)
    f.close()
    line_size_json = json.dumps(line_size)
    return line_size_json

asyncio.get_event_loop().run_until_complete(main())