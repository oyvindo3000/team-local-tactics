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
    print("The server is ready to receive.\n")
    
    # Accept the connections and inform the players 
    # what their player- and color-tag is.
    player1,_ = server.accept()
    print("[red]Player 1 [white]connected.\n")
    player1.send("1".encode())
    player1.send("[red]".encode())
    waiter(player1)

    player2,_ = server.accept()
    print("[blue]Player 2 [white]connected.\n")
    player2.send("2".encode())
    player2.send("[blue]".encode())
    waiter(player2)

    # The time.sleep is used throughout the script to avoid bugs and unwanted behaviour. 
    time.sleep(1)

    # Starts the game session when both players are connected.
    x = Thread(target = gameSession,args=(player1,player2))
    x.start()

def waiter(player: socket):

    # A message while waiting.
    time.sleep(1)
    player.send("\nWelcome to Team-Network-Tactics!\n\nWaiting for opponent...\n".encode())

def gameSession(player1: socket,
                player2: socket):

    # List for selected champs for player 1 and 2.
    sel1 = []
    sel2 = []

    time.sleep(1)  
    player1.send("Opponent found!\n".encode())
    player2.send("Opponent found!\n".encode())       
 
    time.sleep(0.1)  
    player1.send("You are [red]Player 1[white]!\n".encode())
    player2.send("You are [blue]Player 2[white]!\n".encode())

    # Sends a message to the client, that it needs 
    # to handle a message through pickle next.
    time.sleep(0.1)  
    player1.send("pickle".encode())
    player2.send("pickle".encode())

    # Load the champs from the database "champs.txt" through champlistloader.py.
    # Sends it to the client through use of pickle. 
    time.sleep(1)  
    champions = load_some_champs()
    available_champs = helper.available_champs(champions)
    pickle_champs = pickle.dumps(available_champs)
    player1.send(pickle_champs)
    player2.send(pickle_champs)
      
    # The process of selecting champs, 2 champs each.
    for i in range (2):

        time.sleep(0.1)
        player1.send("1".encode())
        player2.send("\nWaiting for [red]Player 1[white] to chose champion...\n".encode())

        # Take a champ as imput from the client, and run through the validChamp function.
        # If the choice is valid, the champ will be appended to the list of selected champs.
        # If not, the validChamp function will send an error message to the client and
        # it will need to select again. The loop is continued until a valid champ is selected.
        while True:
            champname1 = player1.recv(1024).decode()
            if validChamp(champname1, player1, sel1, sel2) == True:
                player1.send("YEAH".encode())
                sel1.append(champname1)
                print("[red]Player 1 [white]chose: " + champname1 + "\n")
                break
        
        output1 = "[red]Player 1[white]: " + champname1
        player2.send(output1.encode())

        time.sleep(0.1)
        player1.send("\nWaiting for [blue]Player 2[white] to chose champion...\n".encode())
        player2.send("2".encode())

        # Same process as above, but with player 2 this time.
        while True:
            champname2 = player2.recv(1024).decode()
            if validChamp(champname2, player2, sel2, sel1) == True:
                player2.send("YEAH".encode())
                sel2.append(champname2)
                print("[blue]Player 2 [white]chose: " + champname2 + "\n")
                break

        output2 = "[blue]Player 2[white]: " + champname2
        player1.send(output2.encode())

    time.sleep(0.1)

    # Get the scores.
    getscores(sel1, sel2, champions, player1, player2)

    time.sleep(0.1)
    print("\nShutting down clients and server.")

    # Sends the "codeword" "finito" to the players to let them know the game is done.
    player1.send("finito".encode())
    player2.send("finito".encode())


def validChamp( champname: str,
                player: socket,
                your: list,
                opponent: list):
    
    # Checks if the selected champ is available.
    if champname not in getChampNames():
        player.send(f'The champion {champname} is not available. Try again.'.encode())

    # Checks if selected champ already is in your own team.
    elif champname in your:
        player.send(f'{champname} is already in your team. Try again.'.encode())

    # Checks if selected champ is in opponents team.
    elif champname in opponent:
        player.send(f'{champname} is in the enemy team. Try again.'.encode())

    # If all the checks pass, the selected champ is a valid choice and we return True. 
    else:
        return True

def getscores(  sel1: list,
                sel2: list,
                champions: dict[Champion],
                player1: socket,
                player2: socket):
    
    # Runs the match.
    match = Match(
        Team([champions[name] for name in sel1]),
        Team([champions[name] for name in sel2])
    )
    match.play()

    # Transform the results to a nice readable layout.
    matchSummary = helper.match_summary(match)

    # Runs through the match summary and sends it to the clients. 
    # This through letting the client know it has to handle it through pickle,
    # and then sending the actual message.
    for i in range(len(matchSummary)):
        time.sleep(0.1)  
        player1.send("\n".encode())
        player2.send("\n".encode())

        time.sleep(0.1)  
        player1.send("pickle".encode())
        player2.send("pickle".encode())

        time.sleep(0.1)
        pickle_champs = pickle.dumps(matchSummary[i])
        player1.send(pickle_champs)
        player2.send(pickle_champs)

        print("\n")
        print(matchSummary[i])
        

server_start()