from typing import Any

import requests
import zbarlight
from PIL import Image
from requests.exceptions import RequestException

from grafeo2.crypto import check_pub_key
from old.core import Product, Producer


def _qrcode_to_pub_key(img: Image) -> str:
    codes = zbarlight.scan_codes('qrcode', img)  # type: str

    print("codes = {}".format(codes))

    if not codes or len(codes) != 1:
        return ""

    pub_key = codes[0].decode('ascii')

    if check_pub_key(pub_key):
        return pub_key
    else:
        return ''


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

    def get_producer_qrcode(self, img: Image) -> Any:
        _pub_key = _qrcode_to_pub_key(img)  # type: str
        print("_pub_key = {}".format(_pub_key))
        if _pub_key:
            _producer = self.get_producer(_pub_key)
            if _producer:
                return _producer

        return None

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

    def get_product_qrcode(self, img: Image) -> Any:
        _pub_key = _qrcode_to_pub_key(img)  # type: str
        print("product _pub_key = {}".format(_pub_key))
        if _pub_key:
            _product = self.get_product(_pub_key)
            if _product:
                return _product

        return None

    def post_producer(self, producer: Producer) -> bool:
        if not producer.is_valid():
            return False

        try:
            _r = requests.post(
                self.url + "/api/product/" + producer.pub_key + ".json",
                               )
        except RequestException:
            return False

        return True

