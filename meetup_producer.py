import random
import socketserver
import sys
import time

some_file_path = 'C:\\dataTest\\ttt '


def iter_file():
    with open(some_file_path, 'r') as f:
        while chunk := f.readline():
            yield chunk


class AlphaTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = iter_file()
        try:
            while True:
                s = ''
                for i, d in enumerate(data):
                    s += d
                    if i > random.randrange(10):
                        print('number of lines to send:', i)
                        break

                b = bytes(s, 'utf-8')
                self.request.sendall(b)
                time.sleep(1)
        except BrokenPipeError:
            print('broken pipe detected', file=sys.stderr)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 301

    server = socketserver.TCPServer((host, port), AlphaTCPHandler)
    print(f'server starting {host}:{port}')
    server.serve_forever()
