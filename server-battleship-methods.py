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
    if(boardArray[x][y] == carrier[0]):
        hit = 1;
        boardArray[x][y] = 'X';
        checkSunk(carrier);
    if(boardArray[x][y] == battleship[0]):
        hit = 1;
        boardArray[x][y] = 'X';
        checkSunk(battleship);
    if(boardArray[x][y] == cruiser[0]):
        hit = 1;
        boardArray[x][y] = 'X';
        checkSunk(cruiser);
    if(boardArray[x][y] == sub[0]):
        hit = 1;
        boardArray[x][y] = 'X';
        checkSunk(sub);
    if(boardArray[x][y] == destroyer[0]):
        hit = 1;
        boardArray[x][y] = 'X';
        checkSunk(destroyer);
    if(hit == 0):
        print("hit=0");
        boardArray[x][y] = 'O';

printBoard();
takeHit(0,0);
takeHit(1,1);
takeHit(9,9);
takeHit(9,8);
printBoard();





