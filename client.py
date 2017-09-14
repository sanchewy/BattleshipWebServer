import sys
import http.client

HOST_NAME = sys.argv[1]
PORT_NUMBER = sys.argv[2]

def send_fire_request(X_COOR, Y_COOR):
    conn = http.client.HTTPConnection(HOST_NAME+":"+PORT_NUMBER)
    conn.request("GET", "/x="+X_COOR+"&y="+Y_COOR)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)

if __name__ == '__main__':
    send_fire_request(sys.argv[3] ,sys.argv[4])
