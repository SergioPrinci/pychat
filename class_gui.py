import tkinter as tk
import socket
import threading

from class_crypto import Crypto, ServerError

class mainWindowGUI:
    #configuration
    mainWindow = tk.Tk()
    mainWindow.title('PYChat')
    mainWindow.geometry('600x800')
    mainWindow.withdraw()

    def __init__(self, username, ipAddress, port, sock, crypto):
        self.mainWindow.deiconify()
        self.username = username
        self.ipAddress = ipAddress
        self.port = port
        self.crypto = crypto
        self.sock = sock
        #mainWindow structure
        self.recvLabel = tk.Label(master = self.mainWindow,
                                    borderwidth=2,
                                    relief='groove',
                                    justify=tk.LEFT,
                                    anchor='nw',
                                    bg='light grey')
        self.recvLabel.place(x=20, y=20, width = 560, height = 718)

        self.clientText = tk.Entry(master = self.mainWindow)
        self.clientText.place(x=20, y=760, width = 500, height=28)

        self.sendButton = tk.Button(master = self.mainWindow,
                                    activebackground = 'grey',
                                    text = 'Send',
                                    command=self.onSendClick)
        self.sendButton.place(x=542, y=760)
        self.mainWindow.bind('<Return>', self.onSendClick)
        
        self.startClient((self.ipAddress, self.port))
        self.initConfig()
        recvThread = threading.Thread(target=self.recvMessage, args=(crypto, sock))
        recvThread.start()

    def onSendClick(self, event=None):
        self.msg = self.clientText.get()
        text = self.recvLabel.cget('text') + '# You | ' + self.msg + '\n'
        self.recvLabel.configure(text = text)
        self.msg = '\n# ' + self.username + ' | ' + self.msg + '\n'
        print("Messaggio inviato e criptato correttamente.\n" + self.msg + "\n")
        self.msg = self.crypto.encode(self.msg)
        self.sock.send(self.msg.encode('utf-8'))
        self.clientText.delete(0,'end')

    def recvMessage(self, crypto : Crypto, sock : socket):
        while True:
            try:
                msg = sock.recv(4096).decode('utf-8')
                if msg != '':
                    msg = crypto.decode(msg)
                    text = self.recvLabel.cget('text') + msg
                    self.recvLabel.configure(text = text)
                    print("Messaggio ricevuto: \n" + msg + "\n")
            except Exception as e:
                print('Error while receiving a message. | ' + str(e))
                raise ServerError('Server closed the connection')

    def startClient(self, addr : tuple):
        try:
            self.sock.connect(addr)
        except Exception as e:
            print('Error while connecting to the server. Please be sure that the ip and the port are right.')
            print(str(e) + '\n\n')
            self.startClient(addr)

    def initConfig(self):
        self.crypto.__setattr__('key', self.sock.recv(10000).decode('utf-8'))

class connectionWindowGUI():
    #configuration
    connectionWindow = tk.Tk()
    connectionWindow.title('PYChat')
    connectionWindow.geometry('300x150')

    def __init__(self, crypto, sock):
        self.crypto = crypto
        self.sock = sock
        #connectionWindow structure
        self.text1 = tk.Label(master = self.connectionWindow, 
                                text = 'IP address',)
        self.text1.place(x=40, y=30)
        self.ipAddressEntry = tk.Entry(master = self.connectionWindow,
                                        text = 'IP Address')
        self.ipAddressEntry.place(x=100, y=30, width=150)

        self.text2 = tk.Label(master = self.connectionWindow, 
                                text = 'Port',)
        self.text2.place(x=40, y=50)
        self.portEntry = tk.Entry(master = self.connectionWindow)
        self.portEntry.place(x=100, y=50, width=150)

        self.text3 = tk.Label(master = self.connectionWindow, 
                                text = 'Username',)
        self.text3.place(x=40, y=70)
        self.usernameEntry = tk.Entry(master = self.connectionWindow)
        self.usernameEntry.place(x=100, y=70, width=150)

        self.okButton = tk.Button(master = self.connectionWindow,
                                    activebackground = 'grey',
                                    text = 'Send',
                                    command=self.onOkClick)
        self.okButton.place(x=130, y=110)
        self.connectionWindow.bind('<Return>', self.onOkClick)

    #methods
    def onOkClick(self, event=None):
        username = str(self.usernameEntry.get())
        ipAddress = str(self.ipAddressEntry.get())
        port = int(self.portEntry.get())
        self.connectionWindow.destroy()
        mainWindow = mainWindowGUI(username, ipAddress, port, self.sock, self.crypto)
        mainWindow.mainWindow.mainloop()
