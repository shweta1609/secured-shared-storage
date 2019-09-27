import socket, ssl
import sqlite3
import crypt
import os
from cryptography.fernet import Fernet


def encrypt_file(filename, key):
    input_file = "temp/" + filename
    output_file = "files/" +filename+".encrypted"
    with open(input_file, 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(output_file, 'wb') as f:
        f.write(encrypted)
    os.remove(input_file)
    return output_file


def decrypt_file(filename, key):
    output_file = "temp/" + filename
    input_file = "files/" +filename+".encrypted"
    with open(input_file, 'rb') as f:
        data = f.read()
    print "Data before decryption:"
    print data
    try:
        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)
    except Exception as e:
        print "Decryption Failed: ", e
    print "Decrypted data:"
    print decrypted
    with open(output_file, 'wb') as f:
        f.write(decrypted)
    return output_file

def save_key(key, filename):
    key_file_loc = "keys/"+filename+"_key.key"
    # with open("server.pub") as file:
    #     server_pub_key = file.read()
    #     fernet = Fernet(server_pub_key)
    #     encrypt_key = fernet.encrypt(key)
    key_file = open(key_file_loc, 'wb')
    # key_file.write(encrypt_key)
    key_file.write(key)
    key_file.close()
    return key_file_loc

def get_key(key_file_loc):
    key_file = open(key_file_loc, 'rb')
    key = key_file.read()
    print  "Key for decryption:"
    print key
    print ""
    key_file.close()
    # with open("server.pub") as file:
    #     server_pub_key = file.read()
    #     fernet = Fernet(server_pub_key)
    #     decrypt_key = fernet.encrypt(key)
    # return decrypt_key
    return key

bindsocket = socket.socket()
bindsocket.bind(('localhost', 10023))
bindsocket.listen(5)
documents_col_list = ['document','swetha', 'sarmistha', 'ahamad', 'location', 'sec_flag', 'key_path']


newsocket, fromaddr = bindsocket.accept()
while True:
    # connstream = ssl.wrap_socket(newsocket,
    #                              server_side=True,
    #                              certfile="server.crt",
    #                              keyfile="server.key")
    data = newsocket.recv(1024)
    if(data.startswith('1')):
        details =  data.split(',')
        user = details[1]
        passwd = details[2]
        crypted_psswd = crypt.crypt(passwd, "salt")
        print user
        conn = sqlite3.connect('3s.db')
        c = conn.cursor()
        t = (user,)
        c.execute("SELECT * FROM user_login WHERE user = ?",t)
        res =  c.fetchone()
        conn.close()
        if not res or crypted_psswd != res[1]:
            newsocket.send("incorrect username or password")
        else:
            newsocket.send("user logged in")

    if(data.startswith('2')):
        user = 'sarmistha'
        filename = data.split(',')[1]
        conn = sqlite3.connect('3s.db')
        c = conn.cursor()
        t = (filename,)
        c.execute("SELECT * FROM documents_info WHERE document = ?", t)
        res = c.fetchone()
        conn.close()
        i = documents_col_list.index(user)
        if res and res[i] in ['owner', 'allowed']:
            encr_file_loc = res[4]
            sec_flag = res[5]
            key_loc = res[6]
            temp_loc = ""
            # if sec_flag == "CONFIDENTIAITY":
            key = get_key(key_loc)
            temp_loc = decrypt_file(filename, key)
            newsocket.send("downloading file")
            newsocket.send(str(os.path.getsize(temp_loc)))
            # newsocket.send("sending file now..")
            with open (temp_loc, 'rb') as f:
                bytes = f.read(1024)
                newsocket.send(bytes)
                while bytes != "":
                    bytes = f.read(1024)
                    newsocket.send(bytes)
            os.remove(temp_loc)
        else:
            newsocket.send("no file access permission")

    if(data.startswith('3')):
        filename = data.split(',')[1]
        sec_flag = data.split(',')[2]
        location = "temp/"+filename
        user = "sarmistha"
        conn = sqlite3.connect('3s.db')
        c = conn.cursor()
        t = (filename, )
        c.execute("SELECT * FROM documents_info WHERE document = ?",t)
        res = c.fetchall()
        # if not res or res[3] in ["owner","allowed"]:
        if not res:
            newsocket.send("uploading file")
            file_length = int(newsocket.recv(1024))
            rec_file_length = 0
            print file_length
            with open(location, 'wb') as f:
                while (rec_file_length < file_length):
                    data = newsocket.recv(1024)
                    print data
                    f.write(data)
                    rec_file_length += len(data)
                    print rec_file_length
                    print file_length
            if sec_flag == "CONFIDENTIAITY":
                key = Fernet.generate_key()
                location = encrypt_file(filename, key)
                key_path = save_key(key, filename)
                t = (filename, location,sec_flag,key_path)
                c.execute("INSERT INTO documents_info VALUES (?,'allowed','owner','',?,?,?)", t)
                conn.commit()
                conn.close()
            elif sec_flag == "INTEGRITY":
                # TODO signing document
                t = (filename, location,sec_flag,key_path)
                c.execute("INSERT INTO documents_info VALUES (?,'allowed','owner','',?,?,?)", t)
                conn.commit()
                conn.close()

        else:
            print res
            newsocket.send("please change filename")

    if(data.startswith('4')):
        filename = data.split(',')[1]
        user = "sarmistha"
        conn = sqlite3.connect('3s.db')
        c = conn.cursor()
        t = (filename, )
        c.execute("SELECT * FROM documents_info WHERE document = ?",t)
        res = c.fetchone()
        location = res[4]
        if res[2] != 'owner':
            newsocket.send("only owner can delete a file")
        else:
            newsocket.send("deleting file")
            t = (filename,)
            c.execute("DELETE FROM documents_info WHERE document=?", t)
            conn.commit()
            os.remove(location)