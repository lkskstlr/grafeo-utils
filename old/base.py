from typing import NamedTuple, Dict
from grafeo2.crypto import generate_key_pair
import abc


"""Separators used for serialization

Separator.field between high level fields
Separator.list within a list
"""
Separators = NamedTuple('Separators', [('field', str), ('list', str)])
separators = Separators(';;', ',,')


"""The current version"""
current_version_major = 0
current_version_minor = 0
current_version_patch = 0


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

    @abc.abstractmethod
    def sign(self) -> bool:
        """Signs of the produc(er/t)
        using the own private key and possible the
        private keys of all inputs"""
        pass
