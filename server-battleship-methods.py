import sys

port = sys.argv[1];
print("Port Number: {!s}".format(port)); 
boardFile = sys.argv[2];
fp = open(boardFile);
board = fp.read()
boardList = board.splitlines();

#initialize board array
boardArray = [0] * 10;
for i in range(len(boardArray)):
    boardArray[i] = [0] * 10;
for i in range(len(boardArray)):
    for j in range(len(boardArray[i])):
        boardArray[i][j] = boardList[i][j];

#prints board array
def printBoard():
    print;
    for i in range(len(boardArray)):
        for j in range(len(boardArray[i])):
            print(boardArray[i][j]),
        print;
    print;

carrier = ['C', 0];
battleship = ['B', 0];
cruiser = ['R', 0];
sub = ['S', 0];
destroyer = ['D', 0];
ships = [carrier, battleship, cruiser, sub, destroyer];

def checkSunk(ship):
    if(ship[1] == 0):
        ship[1] = 1;
    for i in range(len(boardArray)):
        for j in range(len(boardArray[i])):
            if(boardArray[i][j] == ship[0]):
                ship[1] = 0;
    sys.stdout.write('hit=1');
    if(ship[1] == 1):
        print("&sink={!s}".format(ship[0]));
    else:
        print;

def takeHit(x, y):
    hit = 0;
    for ship in range(len(ships)):
        if(boardArray[x][y] == ships[ship][0]):
            hit = 1;
            boardArray[x][y] = 'X';
            checkSunk(ships[ship]);
            break;
    if(hit == 0):
        print("hit=0");
        boardArray[x][y] = 'O';

printBoard();
takeHit(0,0);
takeHit(1,1);
takeHit(1,9);
takeHit(9,9);
takeHit(9,8);
printBoard();





