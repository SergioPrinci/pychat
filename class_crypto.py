from base64 import b64decode, b64encode
from random import randint


# dichiarazione classe
class Crypto:
    # attributi
    key = str()
    server = bool()

    # metodo costruttore
    def __init__(self, server):
        self.server = server
        if self.server:
            try:
                password = "".join([chr(randint(0, 255)) for _ in range(4096)])
                password_bytes = b64encode(password.encode("utf-8"))
                self.key = password_bytes.decode("utf-8")
            except Exception as e:
                print("Error generating private key.\n" + str(e))
            print("Key: " + self.key +
                    "\n---------------------------------------------")
        else:
            pass

    def encode(self, message: str):
        message = message.strip()
        mess, key = list(), int()
        try:
            for i in self.key:
                key += ord(i)
            for c in message:
                if not len(mess)+1 == len(message):
                    mess.append(str(ord(c)*key) + "_")
                else:
                    mess.append(str(ord(c)*key))
            return b64encode("".join(mess).encode("utf-8")).decode("utf-8")
        except Exception as e:
            print("Error encoding the message.\n" + str(e))
            return -1

    def decode(self, message: str):
        mess, key = list(), int()
        message = b64decode(message.encode("utf-8")).decode("utf-8")
        try:
            for i in self.key:
                key += ord(i)
            for c in message.split("_"):
                mess.append(chr(int(int(c)/key)))
            return "".join(mess)
        except Exception as e:
            print("Error decoding the message.\n" + str(e))
            return -1

class ClientError(Exception):
    pass

class ServerError(Exception):
    pass
