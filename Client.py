import socket
def bet(client,Money):
    in_data = client.recv(1024)
    print(in_data.decode())
    out_data = input()
    loop = True
    while loop:
        if ("bet" in out_data):
            client.sendall(bytes(out_data, 'UTF-8'))
            in_data = client.recv(1024)

            print(in_data.decode())
            out_data = input()
            flag = True
            while flag:
                try:
                    Money = Money - int(out_data)
                    client.sendall(bytes(out_data, 'UTF-8'))
                    flag = False
                except:
                    print("Try entering a number")
                    out_data = input()

            loop = False
        elif ("call" in out_data or "fold" in out_data or "check" in out_data):
            client.sendall(bytes(out_data, 'UTF-8'))
            in_data = client.recv(1024)
            print(in_data.decode())
            loop = False
        else:
            print("try entering a check bet call or fold")
            out_data = input()
SERVER = "127.0.0.1"
PORT = 8080
Money = 1000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
in_data =  client.recv(1024)
print(in_data.decode())
out_data = input()
client.sendall(bytes(out_data,'UTF-8'))
in_data =  client.recv(1024)
print(in_data.decode())
out_data = input()
client.sendall(bytes(out_data,'UTF-8'))
  #if out_data=='bye':
   # break
bet(client,Money)
client.close()

