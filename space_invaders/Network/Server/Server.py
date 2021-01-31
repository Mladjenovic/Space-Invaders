import random
import socket
import time
from multiprocessing import Process
from threading import Thread, Lock
from time import sleep

from Network.SocketManager import SocketManager

clients = []
client_ready = 0
clients_died = 0
usernameScoreDict = {}
lock = Lock()


class DeusExProcess(Process):

    def __init__(self, clients):
        super().__init__(target=self.__count__, args=[clients])


    def __count__(self, clients):
        while True:
            time.sleep(15)
            x = random.randrange(200, 900)
            y = random.randrange(50, 350)
            luckyFactor = random.choice(range(-1, 2, 2))
            for client in clients:
                client[0].send_message(f"{luckyFactor}|{x}|{y}")










def startGame():
    global clients
    while True:
        if len(clients) == 2:         # dva je broj igraca
            for client in clients:
                client[0].send_message(f"START GAME||")

            process = DeusExProcess(clients)
            process.start()
            break
        sleep(1)

def proccesingClient(s: socket):
    socket_manager = SocketManager(s)
    global cnt
    global clients
    flag, message, spaceship_image = socket_manager.recv_message()
    username = message
    myUsername = message
    print("-" * 69)
    print(f"{flag}, {username}, {spaceship_image}")
    print("-" * 69)


    for client in clients:
        client[0].send_message(f"NEW CLIENT|{username}|{spaceship_image}")
        print(f"Klijent: {client[1]} | Username: {username}")
        time.sleep(0.2)
        socket_manager.send_message(f"NEW CLIENT|{client[1]}|{client[2]}")

    clients.append((socket_manager, username, spaceship_image))

    print("-"*70)
    print("-"*70)
    print(len(clients))
    print("-"*70)
    print("-"*70)

    while True:
        try:
            flag, username, spaceship_image = socket_manager.recv_message()
            print(f"{flag} { username}")

            if flag == "MOVE LEFT":
                for client in clients:
                    if client[1] != username:
                        client[0].send_message(f"MOVE LEFT|{username}|")

            elif flag == "MOVE RIGHT":
                for client in clients:
                    if client[1] != username:
                        client[0].send_message(f"MOVE RIGHT|{username}|")

            elif flag == "SHOOT":
                bullet_id = spaceship_image
                for client in clients:
                    if client[1] != username:
                        client[0].send_message(f"SHOOT|{username}|{bullet_id}")
            elif flag == "PLAY AGAIN":
                global client_ready
                client_ready += 1
                if client_ready == 2:       # dva je broj igraca
                    for client in clients:
                            client[0].send_message(f"START ANOTHER GAME||")

                    client_ready = 0
            elif flag == "ENEMY DIED":
                global enemies_coordinates
                enemy_id = username
                bullet_id = spaceship_image
                # if spaceceship_id in enemies_coordinates:

                print(f"////////////////////enemy_id: {enemy_id}")
                print(f"////////////////////Bullet_id: {bullet_id[0]}")
                print(f"////////////////////Type of Bullet_id: {type(bullet_id[0])}")


                print("SALJEM KLIJENTU DA JE UBIJEN ENEMY")
                print(enemy_id)
                print(f"---------------->BULLET ID JE {bullet_id}<-----------------------")
                print(f"----------------> TYPE:  {type(bullet_id)}<-----------------------")

                for client in clients:
                    if client[1] != myUsername:
                        client[0].send_message(f"REMOVE ENEMY|{enemy_id}|{bullet_id}")
                    # enemies_coordinates.remove(spaceceship_id)

            elif flag == "NEW LEVEL":
                level = username
                for client in clients:
                    if client[1] != username:
                        client[0].send_message(f"CREATE LEVEL|{level}|")

            elif flag == "UPDATE SCORE":
                scoreIndex = username
                newScore = spaceship_image
                for client in clients:
                    if client[1] != myUsername:
                        client[0].send_message(f"UPDATE USER SCORE|{int(scoreIndex)}|{int(newScore)}")

            elif flag == "USER DIED":
                global clients_died
                clients_died += 1
                score = spaceship_image

                usernameScoreDict[username] = int(score)
               # usernameScoreDict[username] = score
              #  print(f"RIKNUO JEDAN: {username},skor = {score}")
               # print(usernameScoreDict.values())
               # print(usernameScoreDict.keys())

                for client in clients:
                    if client[1] != myUsername:
                        client[0].send_message(f"REMOVE SPACESHIP|{username}|")

                if clients_died == 2:               # broj igraca


                        #print(f"dict pre izbora pobednika= {usernameScoreDict.values()}")
                       # print(f"dict pre izbor: skorcrvenog = {skorCrvenog}, plavog = {skorPlavog} ")
                        #print(usernameScoreDict.keys())
                        #print(max(usernameScoreDict, key=usernameScoreDict.get))
                        usernameOfWinner = max(usernameScoreDict, key=usernameScoreDict.get)
                        print(f"pobednik {usernameOfWinner}")
                       # print(usernameScoreDict.values())

                        for client in clients:
                            client[0].send_message(f"SHOW WINNER|{usernameOfWinner}|{usernameScoreDict[usernameOfWinner]}")

                        clients_died = 0

            elif flag == "HIT BOX":
                if client[1] != myUsername:
                    client[0].send_message(f"HIDE BOX||")









        except Exception as e:
            print(e)
            for client in clients:
                if client[1] == myUsername:
                    clients.remove(client)






if __name__ == '__main__':
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind((socket.gethostname(), 5000))
    listenSocket.listen(4)
    

    print(f"Server is open and waiting for clients at address: {socket.gethostbyname(socket.gethostname())}")
    Thread(target=startGame, args=()).start()

    while True:
        acceptedSocket, address = listenSocket.accept()
        print(f"New clieen has been accepted with address {address}")
        t = Thread(target=proccesingClient, args=[acceptedSocket])
        t.start()
