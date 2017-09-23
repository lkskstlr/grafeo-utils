from typing import NamedTuple, List, Dict, Any
from grafeo.base import version_to_str, Version, current_version, separators
from grafeo.crypto import (
    check_pub_key,
    check_utf8_string,
    check_signature,
    validate_signed_message,
    generate_key_pair,
    sign_message,
    check_priv_key
)


class Producer:
    """Model of a Producer"""

    def __init__(self,
                 pub_key: str,
                 version_major: int,
                 version_minor: int,
                 version_patch: int,
                 name: str,
                 signature: str):
        """Initialize the data for the producer"""

        self.pub_key = pub_key  # type: str
        self.version = Version(
            major=version_major,
            minor=version_minor,
            patch=version_patch
        )  # type: Version
        self.name = name  # type: str
        self.signature = signature  # type: str

    def __str__(self) -> str:
        return "Producer: " + self.name

    def payload(self) -> str:
        """Returns the payload associated with a producer"""

        return separators.field.join([
            self.pub_key,
            version_to_str(self.version),
            self.name])

    def is_valid(self) -> bool:
        """Checks if the Producer is valid

        :return True if producer is correct, False else
        """

        try:
            # Check public key (also done in validate_signed_message)
            if not check_pub_key(self.pub_key):
                return False

            # Check Version
            if self.version != current_version:
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
                message=self.payload(),
                signature=self.signature
            ):
                return False

            return True

        except:

            # If anything goes wrong this is not valid
            return False


"""Local type to handle heterogeneous dictionary return types (not implemented in typing right now)"""
_ProducerAndKey = NamedTuple('_ProducerAndKey', [('producer', Producer), ('priv_key', str)])


def _new_producer(name: str) -> Any:
    """Create a new Producer. All crypto stuff included.

    :param name: The name of the new producer. Must satisfy check_utf8_string(name) = True
    :returns the new producer if everything is ok and an empty Producer in all other cases
    """

    if not check_utf8_string(name):
        return None

    # Generate keys
    _keys = generate_key_pair()  # type: Dict[str, str]

    # Generate producer
    producer = Producer(
        pub_key=_keys['pub_key'],
        name=name,
        version_major=current_version.major,
        version_minor=current_version.minor,
        version_patch=current_version.patch,
        signature=''
    )  # type: Producer

    # Sign off payload
    _payload = producer.payload()  # type: str
    _signature = sign_message(priv_key=_keys['priv_key'], message=_payload)  # type: str

    # Fill Signature
    producer.signature = _signature

    # Check the whole producer
    if not producer.is_valid():
        return None

    return _ProducerAndKey(producer=producer, priv_key=_keys['priv_key'])


class Product:
    """Database Model of a Product"""

    def __init__(self,
                 pub_key: str,
                 version_major: int,
                 version_minor: int,
                 version_patch: int,
                 name: str,
                 producer_pub_key: str,
                 input_pub_keys: List[str],
                 product_signature: str,
                 producer_signature: str,
                 input_signatures: List[str]):

        self.pub_key = pub_key  # type: str
        self.version = Version(
            major=version_major,
            minor=version_minor,
            patch=version_patch
        )  # type: Version
        self.name = name  # type: str
        self.producer_pub_key = producer_pub_key  # type: str
        self.input_pub_keys = input_pub_keys  # type: List[str]
        self.product_signature = product_signature  # type: str
        self.producer_signature = producer_signature  # type: str
        self.input_signatures = input_signatures  # type: List[str]

    def __str__(self) -> str:
        return "Product: " + self.name

    def payload(self) -> str:
        """Returns the payload associated with this product"""

        return separators.field.join([
            self.pub_key,
            version_to_str(self.version),
            self.name,
            self.producer_pub_key,
            separators.list.join(self.input_pub_keys),
        ])

    def is_valid(self) -> bool:
        """Checks if the product is valid

        :returns True if product is correct, False else
        """

        try:
            # Check public key
            if not check_pub_key(self.pub_key):
                return False

            # Check version
            if self.version != current_version:
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
            if not check_signature(self.product_signature):
                return False

            if not check_signature(self.producer_signature):
                return False

            if num_inputs > 0:
                for _sig in self.input_signatures:
                    if not check_signature(_sig):
                        return False

            # Check data integrity
            _message = self.payload()  # type: str

            if not validate_signed_message(
                pub_key=self.pub_key,
                message=_message,
                signature=self.product_signature
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


"""Local type to handle heterogeneous dictionary return types (not implemented in typing right now)"""
_ProductAndKey = NamedTuple('_ProductAndKey', [('product', Product), ('priv_key', str)])


def _new_product(
        name: str,
        producer_pub_key: str,
        producer_priv_key: str,
        input_pub_keys: List[str],
        input_priv_keys: List[str]) -> Any:

    # Check all input
    if not check_utf8_string(name):
        return None

    if not check_pub_key(producer_pub_key):
        return None

    if not check_priv_key(producer_priv_key):
        return None

    if len(input_pub_keys) != len(input_priv_keys):
        return None

    for _pub_key in input_pub_keys:
        if not check_pub_key(_pub_key):
            return None

    for _priv_key in input_priv_keys:
        if not check_pub_key(_priv_key):
            return None

    # Generate keys
    _keys = generate_key_pair()  # type: Dict[str, str]

    # Product
    product = Product(
        pub_key=_keys['pub_key'],
        name=name,
        version_major=current_version.major,
        version_minor=current_version.minor,
        version_patch=current_version.patch,
        producer_pub_key=producer_pub_key,
        input_pub_keys=input_pub_keys,
        product_signature="",
        producer_signature="",
        input_signatures=[]
    )

    # Sign of everything
    _message = product.payload()  # type: str

    # Own key
    product.product_signature = sign_message(
        priv_key=_keys["priv_key"],
        message=_message
    )

    # Producer key
    product.producer_signature = sign_message(
        priv_key=producer_priv_key,
        message=_message
    )

    # Input keys
    product.input_signatures = [
        sign_message(
            priv_key=_priv_key,
            message=_message
        ) for _priv_key in input_priv_keys
    ]

    # Check done product
    if not product.is_valid():
        return None

    return _ProductAndKey(product=product, priv_key=_keys["priv_key"])
