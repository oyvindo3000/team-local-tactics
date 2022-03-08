from socket import socket
import pickle
from rich import print
from rich.prompt import Prompt

# Starts the client and connect it to the server. 
# It also takes a player- and a color-tag.
def client_start():
    sock = socket()
    server_address = ("localhost", 5555)
    sock.connect(server_address)
    player = sock.recv(1024).decode()
    color = sock.recv(1024).decode()
    gamesession(sock, player, color)

def gamesession(sock: socket,
                player: str,
                color: str):

    while True:

        # Recieves a message.
        msg = sock.recv(1024).decode()

        # Decides what to do with the message. Either break, take input,
        # print through pickle or print message directly. 
        if msg == "finito":
            break
        if msg == player:
            while True:
                inputString = f"{color}Player {player}[white]"
                inp = Prompt.ask(inputString)
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