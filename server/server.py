# In built os library for system calls and utilities for sending, receiving and encryption
import os
import utilities

# Assigning host and port through utilities
HOST = utilities.HOST
PORT = utilities.PORT

# Main handle_client function which is called inside the while loop
# Receives data from the client via sock and echo it back


def handle_client(sock, addr):
    # Writing the try, except and finally block inside a while loop to continue executing commands from user after closing the connection
    try:
        # Encryption mode fetched
        data = utilities.recv_msg(sock)

        # Plain text so no encryption required
        if(data == "1"):
            # Receives the command
            msg = utilities.recv_msg(sock)
            print('{}: {}'.format(addr, msg))
            print("Received message: " + msg)
            tokens = msg.split()

            # 5 conditions for 5 commands
            if msg.lower() == "cwd":
                output = utilities.curr_dir()
                utilities.send_msg(sock, output)

            if msg.lower() == "ls":
                path = utilities.curr_dir()
                output = str(utilities.ls(path))
                utilities.send_msg(sock, output)

            if msg.split(" ")[0].lower() == "cd":
                path = msg.split(" ")[1]
                for i in range(2, len(msg.split(" "))):
                    path += " " + msg.split(" ")[i]

                if path in os.listdir() or path == '..':
                    output = utilities.change_dir(path)
                    utilities.send_msg(sock, output)
                # If path doesnt exist in ls then no such directory exists
                else:
                    output = "No such directory exists!"
                    utilities.send_msg(sock, output)

            if msg.split(" ")[0].lower() == "dwd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]
                # Reading characters and encoding them with 'utf-8' and sending them as bytes using sendall
                with open(filename, 'r') as f:
                    while(1):
                        data = f.read(1024)
                        if not data:
                            break
                        data = data.encode('utf-8')
                        sock.sendall(data)
                    f.close()
                # Prompting client if the download gets completed
                msg = "Download Completed!"
                utilities.send_msg(sock, msg)

            if msg.split(" ")[0].lower() == "upd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]
                # Receiving as bytes and decoding them to characters and writing as string
                with open(filename, 'w') as f:
                    while(1):
                        data = sock.recv(1024).decode()
                        if not data:
                            f.close()
                            break
                        f.write(data)
                        # We are receiving as packets of 1024 but in the last iteration when we have less than 1024 we first write that data and then close the file so that the prompt is not written in the file itself
                        if len(data) < 1024:
                            f.close()
                            break
                # Prompting client if the upload gets completed
                msg = "Upload Completed!"
                utilities.send_msg(sock, msg)

        # Mode is Substitute so we will encrypt the message before sending and decrypt the message after receiving
        # Everything else remains same
        elif (data == "2"):

            msg = utilities.recv_msg(sock)
            msg = utilities.decrypt_sub(msg)
            print('{}: {}'.format(addr, msg))
            print("Received message: " + msg)
            tokens = msg.split()
            if msg.lower() == "cwd":
                output = utilities.curr_dir()
                utilities.send_msg(sock, utilities.encrypt_sub(output))

            if msg.lower() == "ls":
                path = utilities.curr_dir()
                output = str(utilities.ls(path))
                utilities.send_msg(sock, utilities.encrypt_sub(output))
            if msg.split(" ")[0].lower() == "cd":
                path = msg.split(" ")[1]
                for i in range(2, len(msg.split(" "))):
                    path += " " + msg.split(" ")[i]

                if path in os.listdir() or path == '..':
                    output = utilities.change_dir(path)
                    utilities.send_msg(
                        sock, utilities.encrypt_sub(output))
                else:
                    output = "No such directory exists!"
                    utilities.send_msg(
                        sock, utilities.encrypt_sub(output))

            if msg.split(" ")[0].lower() == "dwd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]

                with open(filename, 'r') as f:
                    while(1):
                        data = f.read(1024)
                        if not data:
                            break
                        data = utilities.encrypt_sub(data)
                        data = data.encode('utf-8')
                        sock.sendall(data)
                    f.close()
                msg = "Download Completed!"
                utilities.send_msg(sock, utilities.encrypt_sub(msg))

            if msg.split(" ")[0].lower() == "upd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]
                with open(filename, 'w') as f:
                    while(1):
                        data = sock.recv(1024).decode()
                        data = utilities.decrypt_sub(data)
                        if not data:
                            f.close()
                            break
                        f.write(data)
                        if len(data) < 1024:
                            f.close()
                            break

                msg = "Upload Completed!"
                utilities.send_msg(sock, utilities.encrypt_sub(msg))

        # Mode is transpose so we will transpose (reverse) the message before sending and after receiving message
        # Everything else remains same

        elif (data == "3"):

            msg = utilities.recv_msg(sock)
            msg = utilities.transpose(msg)
            print('{}: {}'.format(addr, msg))
            print("Received message: " + msg)
            tokens = msg.split()

            if msg.lower() == "cwd":
                output = utilities.curr_dir()
                utilities.send_msg(sock, utilities.transpose(output))

            if msg.lower() == "ls":
                path = utilities.curr_dir()
                output = str(utilities.ls(path))
                utilities.send_msg(sock, utilities.transpose(output))
            if msg.split(" ")[0].lower() == "cd":
                path = msg.split(" ")[1]
                for i in range(2, len(msg.split(" "))):
                    path += " " + msg.split(" ")[i]

                if path in os.listdir() or path == '..':
                    output = utilities.change_dir(path)
                    utilities.send_msg(
                        sock, utilities.transpose(output))
                else:
                    output = "No such directory exists!"
                    utilities.send_msg(
                        sock, utilities.transpose(output))

            if msg.split(" ")[0].lower() == "dwd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]

                with open(filename, 'r') as f:
                    while(1):
                        data = f.read(1024)
                        if not data:
                            f.close()
                            break
                        data = utilities.transpose(data)
                        data = data.encode('utf-8')
                        sock.sendall(data)

                msg = "Download Completed!"
                utilities.send_msg(sock, utilities.transpose(msg))

            if msg.split(" ")[0].lower() == "upd":
                filename = tokens[1]
                for i in range(2, len(tokens)):
                    filename += " " + tokens[i]
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

                msg = "Upload Completed!"
                utilities.send_msg(sock, utilities.transpose(msg))
        # If user gives other number than 1, 2, or 3 server prints "Invalid Number!"
        else:
            print("Invalid number!")
    # Except block for handling errors and printing them as Socket Error
    except (ConnectionError, BrokenPipeError):
        print('Socket Error')

    finally:
        print('Closed connection to {}'.format(addr))
        sock.close()


# Main block of client executes only if __name__ == '__main__'
if __name__ == '__main__':
    # Creating the listening socket
    listen_sock = utilities.create_listen_socket(HOST, PORT)
    # Address of listening socket
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))
    # Main while loop of server
    while True:
        client_sock, addr = listen_sock.accept()
        print('Connection from {}'.format(addr))
        # Calling the main function which handles the client's requests
        handle_client(client_sock, addr)
