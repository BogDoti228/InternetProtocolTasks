import socket
from concurrent.futures.thread import ThreadPoolExecutor


global ip

PACKET = b'\x13' + b'\x00' * 39 + b'\x6f\x89\xe9\x1a\xb6\xd5\x3b\xd3'


def scan_tcp(port):
    socket.setdefaulttimeout(0.5)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"\n{port}: TCP порт открытый")
        except socket.error:
            f"\n{port}: Ошибка подключения"


def scan_udp(RPORT):
    socket.setdefaulttimeout(2)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as scanner:
        try:
            scanner.sendto(PACKET, (ip, RPORT))
            data, _ = scanner.recvfrom(1024)
            print(f"\n{RPORT}: UDP порт открытый")
        except socket.error:
            pass


def scan(port):
    scan_tcp(port)
    scan_udp(port)


ip = input("введите айпи ")

with ThreadPoolExecutor(200) as pool:
    for port in range(int(input("начало диапазона ")), int(input("конец диапазона ")) + 1):
        pool.submit(scan, port)