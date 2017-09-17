#################################
## CSCI-466: Networks          ##
## Programming Assignment 1    ##
## Battleship Across a Network ##
## --------------------------- ##
## Due 9/18/2017               ##
## Authors:                    ##
## Keinan Balsam               ##
## Kincade Pavich              ##
#################################

import sys
import http.client
import re
from pathlib import Path

HOST_NAME = sys.argv[1]
PORT_NUMBER = sys.argv[2]

def send_fire_request(X_COOR, Y_COOR):
    try:
        conn = http.client.HTTPConnection(HOST_NAME+":"+PORT_NUMBER)
        conn.request("GET", "/x="+X_COOR+"&y="+Y_COOR)
        r1 = conn.getresponse()
        result = r1.read()
        print("Reason:{%s} Status:{%s} Message:{\n%s}" % (r1.reason, r1.status, result))
        ## THIS SECTION UPDATES OUR KNOWLEDGE OF OPPONENT BOARD ##
        if(r1.status == 200): #if shot was successful
            boardFile = Path("opponent-board.txt") #get path to opponent board file
            if boardFile.is_file(): #if it already exists
                boardFile = open("opponent-board.txt") #open it and read it in
                board = boardFile.read()
                boardList = board.splitlines()

                boardArray = [0] * 10
                for i in range(len(boardArray)):
                    boardArray[i] = [0] * 10
                for i in range(len(boardArray)):
                    for j in range(len(boardArray[i])):
                        boardArray[i][j] = boardList[i][j]
            else: # if file does not yet exist (first shot against opponent)
                boardArray = [0] * 10 #populate all squares with underscores
                for i in range(len(boardArray)):
                    boardArray[i] = [0] * 10
                for i in range(len(boardArray)):
                    for j in range(len(boardArray[i])):
                        boardArray[i][j] = "_"
            if "1" in str(result): #if hit
                boardArray[int(X_COOR)][int(Y_COOR)] = "X" #update with X
            if "0" in str(result): #if miss
                boardArray[int(X_COOR)][int(Y_COOR)] = "O" #update with O
            fp = open("opponent-board.txt", "w") # update board file with new values
            for i in range(len(boardArray)):
                for j in range(len(boardArray[i])):
                    fp.write(boardArray[i][j])
                fp.write("\n");
            fp.close()

    except http.client.HTTPException as e:
        print("Error:%s" %(e))

if __name__ == '__main__':
    send_fire_request(sys.argv[3] ,sys.argv[4])
