import socket
import struct
import time

from icmp import IcmpPacket


class Traceroute:
    def __init__(self):
        self._PORT = 80
        self._TTL_MAX_HOP = 30
        self._ttl = 1
        self._TIMEOUT = 3

    def run(self, website: str):
        destination_addr = socket.gethostbyname(website)

        print(
            f'Трассировка маршрута к {website} [{destination_addr}]\n'
            f'с максимальным числом прыжков {self._TTL_MAX_HOP}:\n'
        )

        while True:
            recv_begin_time = time.time()

            receiver = self.__create_receiver_socket()
            send_socket = self.__create_sender_socket()

            received_addr = None
            finished = False
            tries_get_data = 3
            tries_values = []

            send_socket.sendto(IcmpPacket(IcmpPacket.ECHO_REQUEST, 0).pack(), (destination_addr, self._PORT))

            while not finished and tries_get_data > 0:
                try:
                    data, received_addr = receiver.recvfrom(1024)
                    recv_end_time = time.time()

                    finished = True

                    tries_values.append(str(int((recv_end_time - recv_begin_time) * 1000)))
                except socket.timeout:
                    tries_get_data -= 1
                    tries_values.append('*')

            receiver.close()
            send_socket.close()

            for i in range(len(tries_values), 3):
                tries_values.append(tries_values[len(tries_values) - 1])

            for i in range(0, len(tries_values)):
                tries_values[i] = self._format_time(tries_values[i])

            if received_addr is not None:
                received_name = socket.gethostbyname(received_addr[0])

                if received_name == received_addr:
                    print(f'{self._ttl}. {"    ".join(tries_values)} {received_name}')
                else:
                    print(f'{self._ttl}. {"    ".join(tries_values)} {received_name} [{received_addr[0]}]')
            else:
                print(f'{self._ttl}. {"    ".join(tries_values)}  Превышен интервал для ожидания запроса.')

            self._ttl += 1

            if received_addr == destination_addr or self._ttl > self._TTL_MAX_HOP:
                break

    def __create_receiver_socket(self) -> socket:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        recv_socket.settimeout(self._TIMEOUT)

        return recv_socket

    def __create_sender_socket(self) -> socket:
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
        sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, self._ttl)

        return sender_socket

    @staticmethod
    def _format_time(time_data: str) -> str:
        if len(time_data) < 2:
            return f'   {time_data}'

        if len(time_data) < 3:
            return f'  {time_data}'

        if len(time_data) < 4:
            return f' {time_data}'

        return f'{time_data}'
