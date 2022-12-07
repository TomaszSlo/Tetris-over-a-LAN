import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    conn1, address1 = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address1))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        data1 = conn1.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        print("from connected user: " + str(data1))
        #data = input(' -> ')
        conn.send(data1.encode())  # send data to the client
        conn1.send(data.encode())
    conn.close()  # close the connection
    conn1.close()

if __name__ == '__main__':
    server_program()