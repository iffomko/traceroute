import re
import socket


class WhoisDataFinder:
    def __init__(self):
        self.gray_ips = [
            '192.168.',
            '172.16.',
            '10.',
            '127.',
            '169.254.'
        ]

        self._WHOIS_PORT = 43
        self._IANA_ADDRESS = 'whois.iana.org'
        self._LOCAL_TEXT = 'local'
        self._WHOIS_RE = re.compile(r"([A-Za-z\-]+):\s+([^\#\n]+)")

    def is_white_ip(self, ip: str) -> bool:
        for pattern in self.gray_ips:
            if ip.startswith(pattern):
                return False

        return True

    def _get_whois_server(self, address: str) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as whois_sock:
            whois_sock.settimeout(1)
            whois_sock.connect((socket.gethostbyname(self._IANA_ADDRESS), self._WHOIS_PORT))
            whois_sock.send(f'{address}\r\n'.encode())

            try:
                data = self.receive_data(whois_sock)

                return self._parse_whois_response(data.decode()).get('whois', '')
            except (socket.timeout, ValueError):
                return ''

    def get_data_from_whois_server(self, address: str) -> dict:
        address = self._data_or_default(address)

        if not self.is_white_ip(address):
            return {
                'local': True,
                'local_text': self._LOCAL_TEXT
            }

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as whois_socket:
            whois_address = self._get_whois_server(address=address)

            if len(whois_address) == 0:
                return {'local': False}

            whois_socket.settimeout(2)
            whois_socket.connect((whois_address, self._WHOIS_PORT))
            whois_socket.send(f'{address}\r\n'.encode())

            try:
                data = self.receive_data(whois_socket)

                response = self._parse_whois_response(self._data_or_default(data.decode()))
                response['local'] = False

                return response
            except socket.timeout:
                return {'local': False}

    @staticmethod
    def receive_data(sock: socket.socket) -> bytes:
        data = b""

        while True:
            temp_data = sock.recv(1024)

            if not temp_data:
                break

            data += temp_data

        return data

    @staticmethod
    def _data_or_default(data, default=''):
        if data is None:
            return default

        return data

    def _parse_whois_response(self, data: str) -> dict:
        result = re.findall(self._WHOIS_RE, data)

        return {key: value for key, value in result}
