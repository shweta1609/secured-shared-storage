import socket, ssl

port = 10023

bindsocket = socket.socket()
bindsocket.bind(('localhost', port))
bindsocket.listen(5)
print "Server running on port " + str(port)

def do_something(connstream, data):
    print "do_something:", data
    return False

def deal_with_client(connstream):
    data = connstream.read()
    while data:
        if not do_something(connstream, data):
            break
        data = connstream.read()

while True:
    newsocket, fromaddr = bindsocket.accept()
    try:
        connstream = ssl.wrap_socket(newsocket,
                                     server_side=True,
                                     certfile="server.crt",
                                     keyfile="server.key")
    except Exception as e:
        print e


    try:
        deal_with_client(connstream)
    except Exception as e:
        print e
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()