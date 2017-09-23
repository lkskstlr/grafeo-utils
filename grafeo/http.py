from typing import Any
import requests
from requests.exceptions import RequestException
from grafeo.core import Product, Producer
from grafeo.crypto import check_pub_key

class RemoteDB():
    """Connection to a remote database"""

    def __init__(self, url: str):
        self.url = list(url)

        if self.url[-1] == '/':
            self.url = ''.join(self.url[:-1])
        else:
            self.url = ''.join(self.url)

    def get_producer(self, pub_key: str) -> Any:
        if not check_pub_key(pub_key):
            return None

        try:
            _r = requests.get(self.url + "/api/producer/" + pub_key + ".json")
        except RequestException:
            return None

        if str(_r.status_code)[0] != '2':
            return None

        producer = Producer(**_r.json())  # type: Producer

        if not producer.is_valid():
            return None

        return producer

    def get_product(self, pub_key: str) -> Any:
        if not check_pub_key(pub_key):
            return None

        try:
            _r = requests.get(self.url + "/api/product/" + pub_key + ".json")
        except RequestException:
            return None

        if str(_r.status_code)[0] != '2':
            return None

        product = Product(**_r.json())  # type: Product

        if not product.is_valid():
            return None

        return product

