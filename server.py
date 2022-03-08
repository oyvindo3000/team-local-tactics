
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time
import helper
import pickle

from rich import print
from core import Champion, Match, Team

from champlistloader import load_some_champs
from champlistloader import getChampNames

def server_start():
    server = socket(AF_INET,SOCK_STREAM)
    server.bind(("localhost", 5555))
    server.listen()
    print("The server is ready to receive.")
    
    player1,_ = server.accept()
    player1.send("1".encode())
    waiter(player1)
    player2,_ = server.accept()
    player2.send("2".encode())
    waiter(player2)

    time.sleep(1)

    x = Thread(target = gameSession,args=(player1,player2))
    x.start()

def waiter(player: socket):
    time.sleep(1)
    player.send("\nWelcome to Team-Network-Tactics!\n\nWaiting for opponent...\n".encode())

def gameSession(player1: socket,
                player2: socket):

    sel1 = []
    sel2 = []

    time.sleep(1)  
    player1.send("Opponent found!\n".encode())
    player2.send("Opponent found!\n".encode())       
 
    time.sleep(0.1)  
    player1.send("You are [red]Player 1[white]!\n".encode())
    player2.send("You are [blue]Player 2[white]!\n".encode())

    time.sleep(0.1)  
    player1.send("pickle".encode())
    player2.send("pickle".encode())

    time.sleep(1)  
    champions = load_some_champs()
    available_champs = helper.available_champs(champions)
    pickle_champs = pickle.dumps(available_champs)
    player1.send(pickle_champs)
    player2.send(pickle_champs)
      

    for i in range (2):

        time.sleep(0.1)
        player1.send("1".encode())
        player2.send("\nWaiting for [red]Player 1[white] to chose champion...\n".encode())

        while True:
            champname1 = player1.recv(1024).decode()
            if validChamp(champname1, player1, sel1, sel2) == True:
                player1.send("YEAH".encode())
                sel1.append(champname1)
                break
        
        output1 = "[red]Player 1[white]: " + champname1
        player2.send(output1.encode())

        time.sleep(0.1)
        player1.send("\nWaiting for [blue]Player 2[white] to chose champion...\n".encode())
        player2.send("2".encode())

        while True:
            champname2 = player2.recv(1024).decode()
            if validChamp(champname2, player2, sel2, sel1) == True:
                player2.send("YEAH".encode())
                sel2.append(champname2)
                break

        output2 = "[blue]Player 2[white]: " + champname2
        player1.send(output2.encode())

    time.sleep(0.1)
    getscores(sel1, sel2, champions, player1, player2)

    time.sleep(0.1)
    player1.send("finito".encode())
    player2.send("finito".encode())


def validChamp( champname: str,
                player: socket,
                your: list,
                opponent: list):

    if champname in your:
        player.send(f'{champname} is already in your team. Try again.'.encode())
    elif champname in opponent:
        player.send(f'{champname} is in the enemy team. Try again.'.encode())
    elif champname not in getChampNames():
        player.send(f'The champion {champname} is not available. Try again.'.encode())
    else:
        return True

def getscores(  sel1: list,
                sel2: list,
                champions: dict[Champion],
                player1: socket,
                player2: socket):
    
    match = Match(
        Team([champions[name] for name in sel1]),
        Team([champions[name] for name in sel2])
    )
    match.play()

    game_results = helper.match_summary(match)

    for i in range(len(game_results)):
        time.sleep(0.1)  
        player1.send("\n".encode())
        player2.send("\n".encode())

        time.sleep(0.1)  
        player1.send("pickle".encode())
        player2.send("pickle".encode())

        time.sleep(0.1)
        pickle_champs = pickle.dumps(game_results[i])
        player1.send(pickle_champs)
        player2.send(pickle_champs)

server_start()