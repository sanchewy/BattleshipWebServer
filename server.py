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
import datetime
import re
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

HOST_NAME = '0.0.0.0'           # The only way we could find to serve localhost and IP.
PORT_NUMBER = int(sys.argv[1])  # Port to be used
BOARD_DIM = 10                  # Dimension of the board
DIGITS_REG = str(len(str(BOARD_DIM)))
regex = r"/x=\d{1,"+DIGITS_REG+"}&y=\d{1,"+DIGITS_REG+"}$"
p = re.compile(regex)           # Regex to match coordinates in URL

## SETUP ALL SHIPS AND INITIALIZE AS NOT SUNK
carrier = ['C', 0]
battleship = ['B', 0]
cruiser = ['R', 0]
sub = ['S', 0]
destroyer = ['D', 0]
ships = [carrier, battleship, cruiser, sub, destroyer]

## READ THE BOARD AND SET IN AN AN ARRAY STRUCTURE
boardFile = sys.argv[2]
fp = open(boardFile)
board = fp.read()
boardList = board.splitlines()

boardArray = [0] * 10
for i in range(len(boardArray)):
    boardArray[i] = [0] * 10
for i in range(len(boardArray)):
    for j in range(len(boardArray[i])):
        boardArray[i][j] = boardList[i][j]

## UPDATES BOARD AFTER IT HAS BEEN ATTACKED
def writeBoard():
    fp = open(boardFile, "w")
    for i in range(len(boardArray)):
        for j in range(len(boardArray[i])):
            fp.write(boardArray[i][j])
        fp.write("\n");

## SETS UP SHIPS AND DEFINES HIT/SUNK METHODS
def checkSunk(ship, s):
    if(ship[1] == 0): #assume ship has been sunk
        ship[1] = 1
    for i in range(len(boardArray)): #if we find that the ship is still on the board,
        for j in range(len(boardArray[i])):
            if(boardArray[i][j] == ship[0]):
                ship[1] = 0     #not sunk
    if(ship[1] == 1):   # if we freshly sunk the ship
        if(ship[0] == 'C'):
            s.wfile.write(b"hit=1&sink=C") #send hit and sunk
        elif(ship[0] == 'B'):
            s.wfile.write(b"hit=1&sink=B") #send hit and sunk
        elif(ship[0] == 'R'):
            s.wfile.write(b"hit=1&sink=R") #send hit and sunk
        elif(ship[0] == 'S'):
            s.wfile.write(b"hit=1&sink=S") #send hit and sunk
        elif(ship[0] == 'D'):
            s.wfile.write(b"hit=1&sink=D") #send hit and sunk
    else:
        s.wfile.write(b"hit=1") #otherwise just send hit

def isHit(x, y): #returns whether or not that spot has already been attacked
    if(boardArray[x][y] == 'X' or boardArray[x][y] == 'O'):
        return True;
    return False;

def takeHit(x, y, s):
    if(isHit(x, y) == True): #if this location has already been fired at
        s.send_response(410) #HTTP Gone
        s.send_header(b"Content-type", b"text/html")
        s.end_headers()
        s.wfile.write(b"You already fired at this location!")
    else: #if it is a valid, unattacked location
        s.send_response(200) #send HTTP OK
        s.send_header(b"Content-type", b"text/html")
        s.end_headers()
        hit = 0;
        for ship in range(len(ships)): #check if we hit any ships
            if(boardArray[x][y] == ships[ship][0]):
                hit = 1;
                boardArray[x][y] = 'X';
                checkSunk(ships[ship], s); #check if the ship has been sunk
                break;
        if(hit == 0): #if it was a miss
            boardArray[x][y] = 'O';
            s.wfile.write(b"hit=0") #send hit = 0
    writeBoard()

## MAIN REQUEST HANDLER
class RequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        if  s.path == ("/own_board.html"):             # Request for own_board
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            with open("board.txt", "r") as f:
                s.wfile.write(b"<html><head><title>Opponent Shots Record</title></head>")
                s.wfile.write(b"<body><h1>BATTLESHIP</h1><h2>YOUR BOARD</h2>")
                s.wfile.write(b"<p style=\"font-family: 'courier', serif\">")
                s.wfile.write(b"&nbsp;&nbsp;<b>0123456789</b><br>")
                iteration = 0;
                for line in f:
                    if(iteration == 0): #couldnt figure out how to get it to write as a var properly...
                        s.wfile.write(b"<b>0</b> ")
                    elif(iteration == 1):
                        s.wfile.write(b"<b>1</b> ")
                    elif(iteration == 2):
                        s.wfile.write(b"<b>2</b> ")
                    elif(iteration == 3):
                        s.wfile.write(b"<b>3</b> ")
                    elif(iteration == 4):
                        s.wfile.write(b"<b>4</b> ")
                    elif(iteration == 5):
                        s.wfile.write(b"<b>5</b> ")
                    elif(iteration == 6):
                        s.wfile.write(b"<b>6</b> ")
                    elif(iteration == 7):
                        s.wfile.write(b"<b>7</b> ")
                    elif(iteration == 8):
                        s.wfile.write(b"<b>8</b> ")
                    elif(iteration == 9):
                        s.wfile.write(b"<b>9</b> ")
                    iteration = iteration + 1
                    s.wfile.write(b""+line.encode()+b"<br>") #prints each line of board
                s.wfile.write(b"</p><h4>X: Opponent Hits</h4><h4>O: Opponent Misses</h4></body></html>")
            f.close()
        elif s.path == ("/opponent_board.html"):       # Request for opponent_board
            s.send_response(200)
            s.send_header(b"Content-type", b"text/html")
            s.end_headers()
            with open("opponent-board.txt", "r") as f:
                s.wfile.write(b"<html><head><title>Your Shots Record</title></head>")
                s.wfile.write(b"<body><h1>BATTLESHIP</h1><h2>OPPONENT BOARD</h2>")
                s.wfile.write(b"<p style=\"font-family: 'courier', serif\">")
                s.wfile.write(b"&nbsp;&nbsp;<b>0123456789</b><br>")
                iteration = 0;
                for line in f:
                    if(iteration == 0): #couldnt figure out how to get it to write as a var properly...
                        s.wfile.write(b"<b>0</b> ")
                    elif(iteration == 1):
                        s.wfile.write(b"<b>1</b> ")
                    elif(iteration == 2):
                        s.wfile.write(b"<b>2</b> ")
                    elif(iteration == 3):
                        s.wfile.write(b"<b>3</b> ")
                    elif(iteration == 4):
                        s.wfile.write(b"<b>4</b> ")
                    elif(iteration == 5):
                        s.wfile.write(b"<b>5</b> ")
                    elif(iteration == 6):
                        s.wfile.write(b"<b>6</b> ")
                    elif(iteration == 7):
                        s.wfile.write(b"<b>7</b> ")
                    elif(iteration == 8):
                        s.wfile.write(b"<b>8</b> ")
                    elif(iteration == 9):
                        s.wfile.write(b"<b>9</b> ")
                    iteration = iteration + 1
                    s.wfile.write(b""+line.encode()+b"<br>")
                s.wfile.write(b"</p><h4>X: Your Hits</h4><h4>O: Your Misses</h4></body></html>")
            f.close()
        elif p.match(s.path):                           # Request for fire slavo
            match = re.findall(r"(\d{1,"+DIGITS_REG+"})", s.path)
            x, y = int(match[0]), int(match[1])
            print(str(x)+","+str(y))
            if not (0<=x<BOARD_DIM and 0<=y<BOARD_DIM):  # X and Y are not within range of BOARD_DIM
                s.send_response(404)                             # HTTP response = 404
                s.send_header(b"Content-type", b"text/html")
                s.end_headers()
                s.wfile.write(b"Coordinates out of bounds.")
            else:
                takeHit(x, y, s)
        else:
            s.send_response(400) # For all other messages, return a HTTP response = 400.
            s.send_header(b"Content-type", b"text/html")
            s.end_headers()
            s.wfile.write(b"Improperly formated request.")

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), RequestHandler)
    print (datetime.datetime.now(), "Starting Server - %s:%s" % (HOST_NAME, sys.argv[1]))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print (datetime.datetime.now(), "Stopping Server - %s:%s" % (HOST_NAME, sys.argv[1]))
