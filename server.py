import _thread as thread
import socket
import time

from class_crypto import ClientError, Crypto

crypto = Crypto(True) #message is a class with methods to manage and crypt messages
serverSock = socket.socket() #creation of a socket
serverSock.bind(('', 55555)) #bind socket to port
port = serverSock.getsockname()[1] #getting port
clients = []

def startServer(): #starting function
    print('Port in use: ' + str(port))
    print('Waiting for a connection...')
    serverSock.listen(16)

def initConfig(clientInfos : tuple):
    clientSock, _ = clientInfos
    clientSock.send(crypto.__getattribute__('key').encode('utf-8'))

def connectionLoop(clientInfos : tuple):
    clientSock, clientAddr = clientInfos
    while True:
        #receive message
        try:
            msg = clientSock.recv(4096).decode('utf-8')
            for c in clients:
                try:
                    if c[1] != clientAddr:
                        c[0].send(msg.encode('utf-8'))
                        print("Messaggio ricevuto e ritrasmesso correttamente.")
                except Exception as e:
                    print('Error while broadcasting message. Closing connection with client. | ' + str(e))
                    clients.remove(c)
        except Exception:
            print('Error while receiving a message.')
            raise ClientError('Client has crashed or closed connection.')
    clientSock.close()

startServer()
while True:
    clientInfos = serverSock.accept()
    initConfig(clientInfos)
    print(clientInfos[1][0] + ' has connected.')
    clients.append(clientInfos)
    thread.start_new_thread(connectionLoop, (clientInfos,))
serverSock.close()