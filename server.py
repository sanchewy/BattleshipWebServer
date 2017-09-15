import sys
import datetime
import re
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep


HOST_NAME = '0.0.0.0' # The only way we could find to serve localhost and IP.
PORT_NUMBER = int(sys.argv[1])
BOARD_DIM = 10      # Dimension of the board
DIGITS_REG = str(len(str(BOARD_DIM)))
regex = r"/x=\d{1,"+DIGITS_REG+"}&y=\d{1,"+DIGITS_REG+"}$"
p = re.compile(regex)    # Regex to match coordinates in URL

class RequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        if  s.path == ("/own_board.html"):             # Request for own_board
            s.send_response(200)
            s.send_header(b"Content-type", b"text/html")
            s.end_headers()
            with open("board.txt", "r") as f:
                for line in f:
                    s.wfile.write(b"<br>"+line.encode()+b"</br>")
            f.close()
        elif s.path == ("/opponent_board.html"):       # Request for opponent_board
            s.send_response(200)
            s.send_header(b"Content-type", b"text/html")
            s.end_headers()
            with open("opponent_board.txt", "r") as f:
                for line in f:
                    s.wfile.write(b"<br>"+line.encode()+b"</br>")
            f.close()
        elif p.match(s.path):                           # Request for fire slavo
            match = re.findall(r"(\d{1,"+DIGITS_REG+"})", s.path)
            x, y = int(match[0]), int(match[1])
            print(str(x)+","+str(y))
            if not (0<=x<BOARD_DIM and 0<=y<BOARD_DIM):  # X and Y are not within range of BOARD_DIM
                s.send_response(404)                             # HTTP response = 404
                s.send_header(b"Content-type", b"text/html")
                s.wfile.write(b"Coordinates out of bounds.")
                s.end_headers()
            # Check if coordinates have allready been fired upon. board(x,y)=='X'
                # If yes, HTTP response = 410
            # Check if coordinates hit or/and sink
                # Return "hit=1" or "hit=0" or "hit=1&sink={C,B,R,S,D}" HTTP response = 200
        else:                                           # Improperly formatted
            s.send_response(400)                        # For all other messages, return a HTTP response = 400.
            s.send_header(b"Content-type", b"text/html")
            s.wfile.write(b"Improperly formated request.")
            s.end_headers()

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
