import socket 
from threading import Thread

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 8000

server.bind((ip_address,port))

server.listen()

print("Server is running")

clients = []
nicknames = []

def client_thread(con,nickname):
    con.send("Welcome to the CHAT ROOM".encode("utf-8"))
    while True:
        try:
            message = con.recv(2048).decode("utf-8")
            if message:
                print(message)
                brodcast(message,con)
            else:
                remove(con)
                remove_nickname(nickname)

        except:
            continue


def remove(con):
    if con in clients:
        clients.remove(con)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


def brodcast(messageToSend,con):
    for client in clients:
        if client != con:
            try:
                client.send(messageToSend.encode("utf-8"))
            except:
                remove(client)

while True:
    con,addr = server.accept()
    
    con.send("NICKNAME".encode("utf-8"))
    nickname = con.recv(2048).decode("utf-8")

    clients.append(con)
    nicknames.append(nickname)

    message = "{} joined the CHAT ROOM".format(nickname)
    print(message)

    brodcast(message,con)

    new_thread = Thread(target=client_thread,args=(con,nickname))
    new_thread.start()




