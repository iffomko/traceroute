import socket

from enums.parser_enum import ParserEnum
from icmp import IcmpPacket
from trace_view import TraceView
from whois import WhoisDataFinder


class Traceroute:
    def __init__(self, params: dict):
        self._PORT = params.get(ParserEnum.trace_port_key)
        self._TTL_MAX_HOPS = params.get(ParserEnum.ttl_max_key)
        self._TIMEOUT = params.get(ParserEnum.timeout_key)
        self._TARGET = params.get(ParserEnum.target_key)
        self._ttl = 1
        self.trace_view = TraceView()

    def run(self):
        Traceroute.test_for_permissions()

        destination_addr = socket.gethostbyname(self._TARGET)

        print(self.trace_view.get_header(
                website=self._TARGET,
                destination_addr=destination_addr,
                ttl_max_hops=self._TTL_MAX_HOPS
        ))

        while True:
            receiver = self._create_receiver_socket()
            sender = self._create_sender_socket()

            received_addr = None
            finished = False
            tries_get_data = 3

            sender.sendto(b"", (destination_addr, self._PORT))

            while not finished and tries_get_data > 0:
                try:
                    data, received_addr = self.receive_data(receiver)

                    finished = True

                    received_addr = received_addr[0]
                except socket.timeout:
                    tries_get_data -= 1

            receiver.close()
            sender.close()

            whois = WhoisDataFinder()

            print(self.trace_view.get_view_trace(
                finished=finished,
                received_addr=received_addr,
                whois_data=whois.get_data_from_whois_server(received_addr),
                ttl=self._ttl,
                ttl_max_hops=self._TTL_MAX_HOPS
            ))

            self._ttl += 1

            if (received_addr is not None and received_addr == destination_addr) or self._ttl > self._TTL_MAX_HOPS:
                break

    def _create_receiver_socket(self) -> socket:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        recv_socket.settimeout(self._TIMEOUT)

        return recv_socket

    def _create_sender_socket(self) -> socket:
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_TCP)
        sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, self._ttl)

        return sender_socket

    @staticmethod
    def receive_data(sock: socket.socket) -> tuple:
        return sock.recvfrom(1024)

    @staticmethod
    def test_for_permissions():
        socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
