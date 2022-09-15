# Socket for socket functionality, sys for setting host ip address, utilities for sending, receiving and encryption
import socket
import utilities
import sys

# Assigning host and port
HOST = '192.168.56.1'
PORT = utilities.PORT

# Main block of client executes only if __name__ == '__main__'
if __name__ == '__main__':
    # Writing the try, except and finally block inside a while loop to continue taking commands from user after closing the connection
    while True:
        try:
            # creating an INET (IPv4), STREAMing socket (TCP)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connecting to the server on port 4040
            sock.connect((HOST, PORT))
            print('\nConnected to {}:{}'.format(HOST, PORT))
            # Select any encryption : Plaintext / Substitute / Transpose
            data = input("Select any number from 1, 2, and 3: ")
            utilities.send_msg(sock, data)

            # Plain text, so no need of encrytion
            if(data == "1"):
                print("Type message in encrypted mode, enter to send, 'exit' to quit")
                # User's command
                msg = input()
                tokens = msg.split()
                # Breaking out of the loop and closing socket to close the connection
                if msg == 'exit':
                    print("Connection closed!")
                    break
                # If the command is dwd then write the file in user
                elif tokens[0] == "dwd":
                    utilities.send_msg(sock, msg)
                    filename = tokens[1]
                    for i in range(2, len(tokens)):
                        filename = filename + " " + tokens[i]
                # 'w' is used for writing in strings
                    with open(filename, 'w') as f:
                        while(1):
                            data = sock.recv(1024).decode()
                            if not data:
                                break
                            f.write(data)
                        # We are receiving as packets of 1024 but in the last iteration when we have less than 1024 we first write that data and then close the file so that the prompt is not written in the file itself
                            if len(data) < 1024:
                                break
                        f.close()
                    msg = utilities.recv_msg(sock)
                    print(msg)
                # If the command is upd then write the file in user
                elif tokens[0] == "upd":
                    utilities.send_msg(sock, msg)
                    filename = tokens[1]
                    for i in range(2, len(tokens)):
                        filename = filename + " " + tokens[i]
                # 'r' is used for reading in strings
                    with open(filename, 'r') as f:
                        while(1):
                            data = f.read(1024)
                            if not data:
                                break
                            data = data.encode('utf-8')
                            sock.sendall(data)
                        f.close()
                    msg = utilities.recv_msg(sock)
                    print(msg)

                # All the commands except upload, download and exit are handled here
                else:
                    utilities.send_msg(sock, msg)
                    print('Sent message: {}'.format(msg))
                    msg = utilities.recv_msg(sock)
                    print('Received echo: ' + msg)

            # Mode is Substitute so we will encrypt the message before sending and decrypt the message after receiving
            # Everything else remains same
            elif (data == "2"):
                print("Type message, enter to send, 'exit' to quit")
                msg = input()
                tokens = msg.split()

                if msg == 'exit':
                    print("Connection closed!")
                    break
                elif tokens[0] == "dwd":
                    utilities.send_msg(sock, utilities.encrypt_sub(msg))
                    filename = tokens[1]
                    for i in range(2, len(tokens)):
                        filename = filename + " " + tokens[i]
                    with open(filename, 'w') as f:
                        while(1):
                            data = sock.recv(1024).decode()
                            data = utilities.decrypt_sub(data)
                            if not data:
                                break
                            f.write(data)
                            if len(data) < 1024:
                                break
                        f.close()
                        msg = utilities.recv_msg(sock)
                        msg = utilities.decrypt_sub(msg)
                        print(msg)

                elif tokens[0] == "upd":

                    utilities.send_msg(sock, utilities.encrypt_sub(msg))
                    filename = tokens[1]
                    for i in range(2, len(tokens)):
                        filename = filename + " " + tokens[i]

                    with open(filename, 'r') as f:
                        while(1):
                            data = f.read(1024)
                            if not data:
                                break
                            data = utilities.encrypt_sub(data)
                            data = data.encode('utf-8')
                            sock.sendall(data)
                        f.close()
                    msg = utilities.recv_msg(sock)
                    msg = utilities.decrypt_sub(msg)
                    print(msg)
                else:

                    utilities.send_msg(sock, utilities.encrypt_sub(msg))
                    print('Sent message: {}'.format(msg))
                    msg = utilities.recv_msg(sock)
                    msg = utilities.decrypt_sub(msg)
                    print('Received echo: ' + msg)

            # Mode is transpose so we will transpose (reverse) the message before sending and after receiving message
            # Everything else remains same
            elif (data == "3"):
                print("Type message in encrypted mode, enter to send, 'exit' to quit")
                msg = input()
                tokens = msg.split()

                if msg == 'exit':
                    print("Connection closed!")
                    break
                elif tokens[0] == "dwd":

                    utilities.send_msg(sock, utilities.transpose(msg))
                    filename = tokens[1]
                    for i in range(2, len(tokens)):
                        filename = filename + " " + tokens[i]
                    with open(filename, 'w') as f:
                        while(1):
                            data = sock.recv(1024).decode()
                            data = utilities.transpose(data)

                            if not data:
                                f.close()
                                break
                            f.write(data)
                            if len(data) < 1024:
                                f.close()
                                break

                    msg = utilities.recv_msg(sock)
                    msg = utilities.transpose(msg)
                    print(msg)

                elif tokens[0] == "upd":

                    utilities.send_msg(sock, utilities.transpose(msg))
                    filename = tokens[1]
                    for i in range(2, len(tokens)):
                        filename = filename + " " + tokens[i]

                    with open(filename, 'r') as f:
                        while(1):
                            data = f.read(1024)
                            if not data:
                                f.close()
                                break
                            data = utilities.transpose(data)
                            data = data.encode('utf-8')
                            sock.sendall(data)

                    msg = utilities.recv_msg(sock)
                    msg = utilities.transpose(msg)
                    print(msg)
                else:
                    utilities.send_msg(sock, utilities.transpose(msg))
                    print('Sent message: {}'.format(msg))
                    msg = utilities.recv_msg(sock)
                    msg = utilities.transpose(msg)
                    print('Received echo: ' + msg)
            # If anything else is given except 1, 2, or 3
            else:
                print("Please select a valid number!")
        # If connection error then the terminal prints 'Socket Error' after breaking out of the loop and closes the socket
        except ConnectionError:
            print('Socket error')
            sock.close()
            break
        # At the end after executing try or except block the socket is closed
        finally:
            sock.close()
            print('Closed connection to server\n')
