from typing import Dict, List, Any
from .common import *
from .crypto import (
    generate_key_pair,
    check_utf8_string,
    check_pub_key,
    check_priv_key,
    check_signature,
    validate_signed_message,
    sign_message
)
import abc
import warnings
import requests
import os
import pickle
import copy
import pprint


class BaseProd(object):
    """The Base class for Producer and Product"""

    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 pub_key: str = '',
                 version_major: int = current_version_major,
                 version_minor: int = current_version_minor,
                 version_patch: int = current_version_patch,
                 name: str = '',
                 signature: str = ''):
        """Construct new base produc(er/t) with a public key,
        a semantic version, a name and a signature corresponding
        to the public key
        """

        if not pub_key:
            self._generate_key_pair()
        else:
            self.pub_key = pub_key  # type: str
            self.priv_key = ''  # type: str

        self.version_major = version_major  # type: int
        self.version_minor = version_minor  # type: int
        self.version_patch = version_patch  # type: int

        self.name = name  # type: str
        self.signature = signature  # type: str

    def _generate_key_pair(self):
        """Generates a public, private key pair for the produc(er/t)"""
        _pair = generate_key_pair()  # type: Dict[str, str]

        self.pub_key = _pair['pub_key']
        self.priv_key = _pair['priv_key']

    @abc.abstractmethod
    def __str__(self):
        """string representation"""
        pass

    @abc.abstractmethod
    def is_valid(self) -> bool:
        """Checks if the produc(er/t) is valid
        i.e. all data has the right format and
        all signatures are correct
        """
        pass

    @abc.abstractmethod
    def _payload(self) -> str:
        """Turns the class into the specified string"""
        pass


class Producer(BaseProd):
    """A Producer with public key, name etc."""

    def __init__(self,
                 pub_key: str = '',
                 version_major: int = current_version_major,
                 version_minor: int = current_version_minor,
                 version_patch: int = current_version_patch,
                 name: str = '',
                 signature: str = ''):
        """Initialize the data for the producer"""

        BaseProd.__init__(self,
                          pub_key=pub_key,
                          version_major=version_major,
                          version_minor=version_minor,
                          version_patch=version_patch,
                          name=name,
                          signature=signature)

        if check_priv_key(self.priv_key):
            self.sign()

    def __str__(self):
            return "Producer: " + self.name

    def is_valid(self):
        """Checks if the Producer is valid

        :return True if producer is correct, False else
        """

        try:
            # Check public key (also done in validate_signed_message)
            if not check_pub_key(self.pub_key):
                return False

            # Check name
            if not check_utf8_string(self.name):
                return False

            # Check signature (also done in validate_signed_message)
            if not check_signature(self.signature):
                return False

            # Check data integrity
            if not validate_signed_message(
                pub_key=self.pub_key,
                message=self._payload(),
                signature=self.signature
            ):
                return False

            return True

        except:

            # If anything goes wrong this is not valid
            return False

    def sign(self) -> bool:
        if not check_priv_key(self.priv_key):
            warnings.warn('This producer has no valid private key and can thus not generate a signature.')
            return False

        _payload = self._payload()  # type: str

        if not _payload:
            warnings.warn('Thos producers payload is not valid')
            return False

        _signature = sign_message(priv_key=self.priv_key, message=_payload)  # type: str

        # Fill Signature
        self.signature = _signature

        if not self.is_valid():
            warnings.warn('The created signature was not valid')
            self.signature = ''
            return False

        return True

    def _payload(self) -> str:
        """Returns the payload associated with a producer"""

        if not check_pub_key(self.pub_key):
            warnings.warn('Producer has no valid public key.')
            return ''

        if not (self.name and check_utf8_string(self.name)):
            warnings.warn('Producer has no valid name')
            return ''

        return separators.field.join([
            self.pub_key,
            separators.list.join([
                str(self.version_major),
                str(self.version_minor),
                str(self.version_patch)
            ]),
            self.name])


class Product(BaseProd):
    """Database Model of a Product"""

    def __init__(self,
                 pub_key: str = '',
                 version_major: int = current_version_major,
                 version_minor: int = current_version_minor,
                 version_patch: int = current_version_patch,
                 name: str = '',
                 signature: str = '',
                 producer_pub_key: str = '',
                 input_pub_keys: List[str] = None,
                 producer_signature: str = '',
                 input_signatures: List[str] = None):

        BaseProd.__init__(self,
                          pub_key=pub_key,
                          version_major=version_major,
                          version_minor=version_minor,
                          version_patch=version_patch,
                          name=name,
                          signature=signature)

        self.producer_pub_key = producer_pub_key  # type: str
        self.producer_signature = producer_signature  # type: str
        if input_pub_keys:
            self.input_pub_keys = input_pub_keys  # type: List[str]
        else:
            self.input_pub_keys = []

        if input_signatures:
            self.input_signatures = input_signatures  # type: List[str]
        else:
            self.input_signatures = []

    def __str__(self) -> str:
        return "Product: " + self.name

    def is_valid(self) -> bool:
        """Checks if the product is valid

        :returns True if product is correct, False else
        """

        try:
            # Check public key
            if not check_pub_key(self.pub_key):
                return False

            # Check name
            if not check_utf8_string(self.name):
                return False

            # Check Inputs
            try:
                num_inputs = len(self.input_pub_keys)  # type: int
            except TypeError:
                num_inputs = 0

            try:
                _num_inputs = len(self.input_signatures)  # type: int
            except TypeError:
                _num_inputs = 0

            if num_inputs != _num_inputs:
                return False

            # Check Signatures
            if not check_signature(self.signature):
                return False

            if not check_signature(self.producer_signature):
                return False

            if num_inputs > 0:
                for _sig in self.input_signatures:
                    if not check_signature(_sig):
                        return False

            # Check data integrity
            _message = self._payload()  # type: str

            if not validate_signed_message(
                pub_key=self.pub_key,
                message=_message,
                signature=self.signature
            ):
                return False

            if not validate_signed_message(
                pub_key=self.producer_pub_key,
                message=_message,
                signature=self.producer_signature
            ):
                return False

            if num_inputs > 0:
                for _pub_key, _sig in zip(self.input_pub_keys, self.input_signatures):
                    if not validate_signed_message(
                        pub_key=_pub_key,
                        message=_message,
                        signature=_sig
                    ):
                        return False

            return True

        except:

            # If anything goes wrong this is not valid
            return False

    def sign(self, producer_priv_key: str, input_priv_keys: List[str]) -> bool:

        # Check self
        if not check_utf8_string(self.name):
            return False

        if not check_priv_key(self.priv_key):
            return False

        if not check_pub_key(self.pub_key):
            return False

        # Check Producer
        if not check_pub_key(self.producer_pub_key):
            return False

        if not check_priv_key(producer_priv_key):
            return False

        # Check Inputs
        if self.input_pub_keys:
            _num_inputs1 = len(self.input_pub_keys)
        else:
            _num_inputs1 = 0

        if input_priv_keys:
            _num_inputs2 = len(input_priv_keys)
        else:
            _num_inputs2 = 0

        if _num_inputs1 != _num_inputs2:
            return False

        if _num_inputs1 > 0:
            for _pub_key in self.input_pub_keys:
                if not check_pub_key(_pub_key):
                    return False

            for _priv_key in input_priv_keys:
                if not check_pub_key(_priv_key):
                    return False

        # Sign of everything
        _message = self._payload()  # type: str

        # Own key
        self.signature = sign_message(
            priv_key=self.priv_key,
            message=_message
        )

        # Producer key
        self.producer_signature = sign_message(
            priv_key=producer_priv_key,
            message=_message
        )

        # Input keys
        self.input_signatures = [
            sign_message(
                priv_key=_priv_key,
                message=_message
            ) for _priv_key in input_priv_keys
        ]

        # Check done product
        if not self.is_valid():
            return False

        return True

    def _payload(self) -> str:
        """Returns the payload associated with this product"""

        return separators.field.join([
            self.pub_key,
            separators.list.join([
                str(self.version_major),
                str(self.version_minor),
                str(self.version_patch)
            ]),
            self.name,
            self.producer_pub_key,
            separators.list.join(self.input_pub_keys),
        ])


def new_product(name: str, producer: Producer, inputs: List[Product]) -> Product:
    product = Product(
        name=name,
        producer_pub_key=producer.pub_key,
        input_pub_keys=[_p.pub_key for _p in inputs]
    )

    product.sign(
        producer_priv_key=producer.priv_key,
        input_priv_keys=[_p.priv_key for _p in inputs]
    )

    return product


class BaseDB(abc.ABC):
    """Base class for a local or remote database connection"""

    @abc.abstractmethod
    def get_producer(self, pub_key: str) -> Any:
        """Get a specific producer from the Database"""
        pass

    @abc.abstractmethod
    def get_product(self, pub_key: str) -> Any:
        """Get a specific product from the Database"""
        pass

    @abc.abstractmethod
    def post(self, prod: BaseProd) -> bool:
        """Post a producer or product to the database"""
        pass


class RemoteDB(BaseDB):

    def __init__(self, url: str):
        self.url = list(url)

        if self.url[-1] == '/':
            self.url = ''.join(self.url[:-1])
        else:
            self.url = ''.join(self.url)

    def get_producer(self, pub_key: str):
        if not check_pub_key(pub_key):
            return None

        try:
            _r = requests.get(self.url + "/api/producer/" + pub_key + ".json")
        except requests.RequestException:
            return None

        if str(_r.status_code)[0] != '2':
            return None

        producer = Producer(**_r.json())  # type: Producer

        if not producer.is_valid():
            return None

        return producer

    def get_product(self, pub_key: str):
        if not check_pub_key(pub_key):
            return None

        try:
            _r = requests.get(self.url + "/api/product/" + pub_key + ".json")
        except requests.RequestException:
            return None

        if str(_r.status_code)[0] != '2':
            return None

        product = Product(**_r.json())  # type: Product

        if not product.is_valid():
            return None

        return product

    def post(self, prod: BaseProd) -> bool:
        if not prod.is_valid():
            return False

        if isinstance(prod, Producer):
            _r = requests.post(
                url= self.url + "/api/producer/",
                json=prod.__dict__
            )
        elif isinstance(prod, Product):
            _r = requests.post(
                url= self.url + "/api/product/",
                json=prod.__dict__
            )
        else:
            return False

        if str(_r.status_code)[0] != '2':
            return False

        return True

    def post_producer(self, name: str) -> bool:
        _producer = Producer(name=name)
        return self.post(_producer)

    def post_product(self, name: str, producer: Producer, inputs: List[Product]) -> bool:
        _product = new_product(name=name, producer=producer, inputs=inputs)
        return self.post(_product)


class LocalDB(BaseDB):

    def __init__(self, folderpath: str='/Users/lukas/'):
        self._filename = os.path.abspath(os.path.join(
            folderpath,
            'grafeo_local_db.p'
        ))

        if not os.path.exists(self._filename):
            self._data = {
                'producers': {},
                'products': {}
            }
        else:
            self._data = pickle.load(open(self._filename, "rb" ))

    def __del__(self):
        pickle.dump(self._data, open(self._filename,"wb"))

    def _clean(self):
        os.remove(self._filename)
        self._data = {
                'producers': {},
                'products': {}
            }

    def print(self):
        pprint.pprint(self._data)

    def get_producer(self, pub_key: str):
        return copy.deepcopy(self._data['producers'].get(pub_key))

    def get_product(self, pub_key: str):
        return copy.deepcopy(self._data['products'].get(pub_key))

    def post(self, prod: BaseProd) -> bool:
        if not prod.is_valid():
            return False

        if isinstance(prod, Producer):
            self._data['producers'][prod.pub_key] = copy.deepcopy(prod)
        elif isinstance(prod, Product):
            self._data['products'][prod.pub_key] = copy.deepcopy(prod)
        else:
            return False

        return True

