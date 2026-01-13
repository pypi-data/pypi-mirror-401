# pylint: skip-file
from socket_cyg.socket_client import SocketClient


if __name__ == "__main__":

    client = SocketClient("192.168.6.6", 9102)
    if client.connect():
        try:
            result = client.send_data(b"TRIGGER")
            print(result)
        finally:
            client.disconnect()