import socket


class TraceView:

    def _format_number_trace(self, number: str, ttl_max_hops: int) -> str:
        return f'{number}.{self._generate_spaces(str(ttl_max_hops), number)}'

    def get_view_trace(
            self,
            finished: bool,
            received_addr: str,
            whois_data: dict,
            ttl: int,
            ttl_max_hops: int
    ):
        number_trace = self._format_number_trace(str(ttl), ttl_max_hops)

        if finished:
            received_name = socket.gethostbyname(received_addr)

            if whois_data.get('local'):
                return f'{number_trace} ' \
                       f'{received_name}\r\n' \
                       f'{whois_data.get("local_text")}'

            whois_list = [
                self._data_or_default(whois_data.get('netname')),
                self._data_or_default(whois_data.get('origin')),
                self._data_or_default(whois_data.get('country'))
            ]

            while '' in whois_list:
                whois_list.remove('')

            return f'{number_trace} ' \
                   f'{received_name} {f"[{received_addr}]" if received_name != received_addr else ""}\r\n' \
                   f'{", ".join(whois_list)}'
        else:
            return f'{number_trace} *\r\n'

    @staticmethod
    def get_header(website: str, destination_addr: str, ttl_max_hops: int) -> str:
        return f'Трассировка маршрута к {website} [{destination_addr}]\n' \
               f'с максимальным числом прыжков {ttl_max_hops}:\n'

    @staticmethod
    def _generate_spaces(comparable_data: str, data: str) -> str:
        spaces = []

        for i in range(0, len(comparable_data) - len(data)):
            spaces.append(' ')

        return "".join(spaces)

    @staticmethod
    def _data_or_default(data, default=''):
        if data is None:
            return default

        return data
