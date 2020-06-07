import socket, threading

users = {"Amy" : "11", "Gilda" : "333", "Mon" : "22"}
userMoney = {"Amy" : "1000", "Gilda" : "1000", "Mon" : "1000"}
Players = []
Threads = []
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    def run(self):
        print ("Connection from : ", clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        username = ''
        password = ''
        data = self.csocket.recv(2048)
        user = data.decode()
        print("from client", username)
        userandpass = user.split("#")
        print(userandpass)
        try:
            if (users[userandpass[0]] !=  userandpass[1]):
                self.csocket.send("password incorrect".encode())
                print("pass incorrect to client",clientAddress)
            else:
                self.csocket.send("welcome to poker!".encode())
                print("connection succeed with", clientAddress)
                ListOfPlayer = [userandpass[0], userandpass[1], userMoney[userandpass[0]]]
                Players.append(ListOfPlayer)
                self.csocket.send(userMoney[userandpass[0]].encode())
        except:
                self.csocket.send("username incorrect".encode())
                print("username incorrect to client", clientAddress)

        #sending him to the table, waiting for other clients.
        print ("Client at ", clientAddress , " disconnected...")

    def earlyBets(self):
        flag = True
        while (flag):
            messege = "check, bet, call or fold? "
            self.csocket.send(messege.encode())
            data = self.csocket.recv(2048)
            msg = data.decode()
            if ("check" in msg):
                print("client checked")
                messege = "check"
                self.csocket.send(messege.encode())
                flag = False
            elif ("fold" in msg):
                print("client fold")
                messege = "fold"
                self.csocket.send(messege.encode())
                flag = False
            elif ("call" in msg):
                print("client putted the same amount as the amount wanted")
                messege = "call"
                self.csocket.send(messege.encode())
                flag = False
            elif ("bet" in msg):
                messege = "how much?"
                self.csocket.send(messege.encode())
                data = self.csocket.recv(2048)
                msg = data.decode()
                print("the client bets" ,msg)
                flag = False



LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while len(Players)<1:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    Threads.append(newthread)
    newthread.run()

data = clientsock.recv(2048)
print(data.decode())