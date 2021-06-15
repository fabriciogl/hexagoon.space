#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import requests
from typing import Dict, Union


class ConectorRequest:
    """
    Classe para gerenciar as requisições, inclusive com a gestão de proxies, se necessário.
    """

    def __init__(self, timeout: int = 60, proxy: bool = False, header: bool = False) -> None:
        """

        Atributtes:
            proxy: (boolean) informa se deseja realizar uma requisição com proxy
            header (boolean) informa se deseja sobrescrever o header
            proxies: (dict)  dicionário de schemas para a proxy
            timeout: (int)   valor para ser passado como timeout da requisição
        """

        self.proxy = proxy
        self.header = header
        self.timeout = timeout

        # Criação das credenciais da API de proxy
        proxy_host = "proxy.crawlera.com"
        proxy_port = "8010"
        proxy_auth = "42be2ce98d844343bbe9a0a397edbd48:"  # Make sure to include ':' at the end
        proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
                   "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

        self.proxies = proxies
        self.verify = 'Certificados/crawlera-ca.crt'

    def request_get(self, url: str) -> requests.Response:
        """

        Args:
            url:  (string) Endereço para ser consultado

        Returns:  (response) Resultado da consulta a url

        """

        # Cabeçalho da requisição
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36}',
            'X-Crawlera-Timeout': '60000'}

        if self.proxy and self.header:

            return requests.get(url, proxies=self.proxies, headers=headers, verify=False, timeout=self.timeout)

        elif self.proxy:

            return requests.get(url, proxies=self.proxies, verify=False, timeout=self.timeout)

        elif self.header:

            return requests.get(url, headers=headers, verify=False, timeout=self.timeout)

        else:

            return requests.get(url)

    def request_post(self, url: str, formulario: Dict[str, Union[str, None, int]]) -> requests.Response:
        """

        Args:
            url:        (string)              Endereço para ser consultado
            formulario: (dicionário)          Formulário contendo os parametros post

        Returns:        (request)             Resultado da consulta a url

        """

        # Cabeçalho da requisição
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36}',
            'X-Crawlera-Timeout': '60000'}

        if self.proxy and self.header:

            return requests.post(url, data=formulario, proxies=self.proxies, headers=headers, verify=False, timeout=self.timeout)

        elif self.proxy:

            return requests.post(url, data=formulario, proxies=self.proxies, verify=False, timeout=self.timeout)

        elif self.header:

            return requests.post(url, data=formulario, headers=headers, verify=False, timeout=self.timeout)

        else:

            return requests.post(url, data=formulario, timeout=self.timeout)
