from website import create_app
import socket
import os

app = create_app()

if __name__ == '__main__':
    gw = os.popen("ip -4 route show default").read().split()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw[2], 0))
    ipaddr = s.getsockname()[0]
    app.run(host=ipaddr, debug=True)
    print(ipaddr)
