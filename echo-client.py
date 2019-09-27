import socket, ssl, pprint
import os

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Require a certificate from the server. We used a self-signed certificate
# so here ca_certs must be the server certificate itself.
# ssl_sock = ssl.wrap_socket(s,
#                            ca_certs="server.crt",
#                            cert_reqs=ssl.CERT_REQUIRED)

ssl_sock.connect(('localhost', 10023))



def start_session(hostname, port_num):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Require a certificate from the server. We used a self-signed certificate
    # so here ca_certs must be the server certificate itself.
    try:
        ssl_sock = ssl.wrap_socket(s,
                                   ca_certs="server.crt",
                                   cert_reqs=ssl.CERT_REQUIRED)
        ssl_sock.connect((hostname, port_num))
        # ssl_sock.connect(('localhost', 10023))
    except Exception as e:
        print e
        print "Connection Failed"
        exit()

    print "Successfully connected to server"
    return ssl_sock

# ssl_sock = start_session('localhost', 10023)

def user_login(UID, UserPrivateKey):
    to_send = "1," + str(UID) + "," + str(UserPrivateKey)
    # ssl_sock.send("1,sarmistha,sarmistha")
    ssl_sock.send(to_send)
    print ssl_sock.recv(1024)

def checkout(filename):
    to_send = "2," +filename
    ssl_sock.send(to_send)
    data = ssl_sock.recv(1024)
    print data
    if data == "no file access permission":
        return
    # file_length = int(ssl_sock.recv(1024))
    # rec_file_length = 0
    file_path = "client_files/"+filename
    with open(file_path, 'w') as f:
        # while (rec_file_length < file_length):
        data = ssl_sock.recv(1024)
        print data
        f.write(data)
            # rec_file_length += len(data)
    print "downloaded file"

def check_in(filename, sec_flag):
    to_send = "3," + filename + "," + sec_flag
    ssl_sock.send(to_send)
    data = ssl_sock.recv(1024)
    if (data == "please change filename"):
        print data
        return
    ssl_sock.send(str(os.path.getsize(filename)))
    with open (filename, 'rb') as f:
        bytes = f.read(1024)
        ssl_sock.send(bytes)
        while bytes != "":
            bytes = f.read(1024)
            ssl_sock.send(bytes)

def safe_delete(filename):
    to_send = "4," + filename
    ssl_sock.send(to_send)
    data = ssl_sock.recv(1024)
    print data


# safe_delete('nnewfile.txt')

# user_login("sarmistha", "sarmistha")
# check_in("server.py", "CONFIDENTIAITY")
checkout("server.py")

