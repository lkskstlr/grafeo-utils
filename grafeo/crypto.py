import nacl.signing
import nacl.encoding
import nacl.exceptions

from typing import NamedTuple, Dict

from grafeo.base import version_to_str, Version, current_version, separators


def _check_string(s: str) -> bool:
    """Check if s is a string

    :param s: string to check
    :returns True if s is a string
    """

    return isinstance(s, str)


def _check_hex_string(s: str) -> bool:
    """Checks if s is a valid hex-string

    :param s: string to check
    :returns True if s is a hex-string
    """

    if not _check_string(s):
        return False

    if any((_letter not in set('0123456789abcdef')) for _letter in s):
        return False

    return True


def check_utf8_string(s: str) -> bool:
    """Check if a utf-8 string contains no separators

    :param s: string to check
    :returns True if s is a valid utf 8 string, i.e. does not contain the separators we use
    """
    if not _check_string(s):
        return False

    if separators.field in s:
        return False

    if separators.list in s:
        return False

    # @todo make generic
    if s[0] == ';' or s[0] == ',' or s[-1] == ';' or s[-1] == ',':
        return False

    return True


def check_pub_key(pub_key: str) -> bool:
    """Check if s is a valid hex-string representation of a public key

    :param pub_key: string to check
    :returns True if s is a valid public key (i.e. right character set, right length)
    """

    if not _check_hex_string(pub_key):
        return False

    # the public keys have a length of 32 bytes
    # Each byte is encoded by two chars
    if len(pub_key) != 64:
        return False

    return True


def check_priv_key(priv_key: str) -> bool:
    """Checks validity of private key

    :param priv_key: private key to be checked
    :returns True if private key is correct
    """

    if not _check_hex_string(priv_key):
        return False

    # the private keys have a length of 32 bytes
    # Each byte is encoded by two chars
    if len(priv_key) != 64:
        return False

    return True


def generate_key_pair() -> Dict[str, str]:
    """Generates a public-private key pair as hex-strings

    :returns a dict with the fields 'pub_key' and 'oriv_key'
    """

    signing_key = nacl.signing.SigningKey.generate()  # type: nacl.signing.SigningKey

    private_key = nacl.encoding.HexEncoder.encode(signing_key._seed)  # type: bytes
    public_key = nacl.encoding.HexEncoder.encode(signing_key.verify_key._key)  # type: bytes

    return {
        "pub_key": public_key.decode("ascii"),
        "priv_key": private_key.decode("ascii")
    }


def check_signature(signature: str) -> bool:
    """Check if the signature is valid

    :param signature: signature to be checked
    :returns True if the signature is technically correct
    """
    if not _check_hex_string(signature):
        return False

    # each byte (=8bits) is encoded by two characters
    # signature has 64 bytes
    if len(signature) != 128:
        return False

    return True


def validate_signed_message(
        pub_key: str,
        message: str,
        signature: str) -> bool:
    """Checks if the triple key, data, signature is valid

    This method checks the types of all three inputs for their type

    :param pub_key: The public key to check the signature against (hex-string)
    :param message: The message for which the signature was alegedly constructed (a string)
    :param signature: The alleged signature of the message with the private key (hex-string)
    :returns True if the triple is correct
    """

    # Check Types
    if not check_pub_key(pub_key):
        return False
    if not _check_string(message):
        return False
    if not check_signature(signature):
        return False

    # Convert to bytes
    message_bytes = message.encode('utf-8')  # type: bytes
    pk_bytes = nacl.encoding.HexEncoder.decode(pub_key)  # type: bytes
    signature_bytes = nacl.encoding.HexEncoder.decode(signature)  # type: bytes

    # Check with lib sodium
    verify_key = nacl.signing.VerifyKey(pk_bytes)  # type: nacl.signing.VerifyKey

    try:
        verify_key.verify(smessage=message_bytes, signature=signature_bytes)
        return True
    except nacl.exceptions.BadSignatureError:
        return False


def sign_message(priv_key: str, message: str) -> str:
    """Sign the message message with the key

    :param priv_key: the private key
    :param message: the message to be signed
    :returns the signature of the message
    """

    # Change to bytes
    _message_bytes = message.encode('utf8')  # type: bytes
    _priv_key_bytes = nacl.encoding.HexEncoder.decode(priv_key)  # types: bytes
    _signing_key = nacl.signing.SigningKey(seed=_priv_key_bytes)  # types: nacl.signing.SigningKey

    _signed = _signing_key.sign(_message_bytes)  # type: nacl.signing.SignedMessage

    signature = nacl.encoding.HexEncoder.encode(_signed._signature).decode('ascii')  # types: str

    return signature
