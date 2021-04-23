import tkinter as tk
import socket
import threading
import sys

from class_crypto import Crypto, ServerError
from class_gui import connectionWindowGUI

crypto = Crypto(False)
sock = socket.socket()

connectionWindow = connectionWindowGUI(crypto, sock)
connectionWindow.connectionWindow.mainloop()