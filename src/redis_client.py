import socket
class RedisClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = self._connect(host, port)

    def _connect(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((host, port))
        return server
    
    def _parse_response(self, response):
        response = response.strip()
        if response ==  '$None':
            return None
        if response.startswith('-ERR'):
            return None
        return response[1:]

    def set(self, key, value):
        command = "SET" + " " + key + " " + value+ "\n"
        self.server.send(command.encode())
        response = self.server.recv(1024).decode()
        return self._parse_response(response)

    def get(self, key):
        command = "GET" + " " + key + "\n"
        self.server.send(command.encode())
        response = self.server.recv(1024).decode()
        return self._parse_response(response)
    
    def incr(self, key):
        command = "INCR" + " " + key + "\n"
        self.server.send(command.encode())
        response = self.server.recv(1024).decode()
        return self._parse_response(response)
    
    def close(self):
        self.server.close()


        