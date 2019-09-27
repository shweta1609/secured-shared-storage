import socket, ssl, pprint




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
    # print repr(ssl_sock.getpeername())
    # print ssl_sock.cipher()
    # print pprint.pformat(ssl_sock.getpeercert())

    # ssl_sock.write("boo!")
    return ssl_sock


def stop_session(ssl_sock):
    try:
        ssl_sock.write("Closing connection")
    except Exception as e:
        print "Connection already dead..." + str(e)
        exit()
    checked_out = True #temp val set
    # checked_in => get some flag from check_in function
    if checked_out is True:
        # call check_in to send the updated document to the server
        checked_in = True
        if checked_out is True:
            checked_in = False

    text = ssl_sock.close()
    if text is None:
        print "Socket closed!"
    else:
        print "Error closing connection"


sock = start_session('localhost', 10023)

# sock.close()

stop_session(sock)
