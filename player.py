from socket import socket
import pickle
from rich import print
from rich.prompt import Prompt

def client_start():
    sock = socket()
    server_address = ("localhost", 5555)
    sock.connect(server_address)
    player = sock.recv(1024).decode()
    gamesession(sock, player)

def gamesession(sock: socket,
                player: str):

    while True:
        msg = sock.recv(1024).decode()
        if msg == "finito":
            break
        if msg == player:
            while True:
                if player == "1":
                    test = "[red]Player " + player + "[white]"
                else:
                    test = "[blue]Player " + player + "[white]"

                inp = Prompt.ask(test)
                sock.send(inp.encode())
                validation = sock.recv(1024).decode()
                if validation == "YEAH":
                    break
                else:
                    print(validation)

        elif msg == "pickle":
            pckle = sock.recv(4096)
            output_pckle = pickle.loads(pckle)
            print(output_pckle)
        else:
            print(msg)

client_start()