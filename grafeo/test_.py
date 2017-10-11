from .crypto import (
    _check_string,
    _check_hex_string,
    check_utf8_string,
    check_pub_key,
    check_priv_key,
    generate_key_pair,
    sign_message,
    check_signature,
    validate_signed_message,

)
from .common import separators


test_data = {
    'strings': [
        'I am a weird string |{]}][|¢[|    漢語',
    ],

    'not_strings': [
        None,
        {'a': 1},
        b'I am a weird string',
    ],

    'hex_strings': [
        "0123456789abcdef23434623534523423"
    ],

    'not_hex_strings': [
        "0123456789abcdef23434623534523423 ",
        " 0123456789abcdef23434623534523423",
        "0123456789abcdeg23434623534523423"
    ],

    'utf8_strings': [
        'I am a weird string |{]}][|¢[|     漢語',
        'I am a weird string |{]}][|¢[|     漢語' + ';' + "a",
    ],

    'not_utf8_strings': [
        'I am a weird string |{]}][|¢[|     漢語' + ';',
        ';' + 'I am a weird string |{]}][|¢[|     漢語',
        'I am a weird string |{]}][|¢[|     漢語' + separators.field + "a",
        'I am a weird string |{]}][|¢[|     漢語' + separators.list + "a",
    ],

    'keys': [
        '96f7acd205a1487f305577be02ca861de1f8d1295c7b0e75e2292b8ba2e365db',
        '4cf8aa06fdaa8f166af6fdd84b8e55270f7efc11cdb7f175c7eb0d9c85bebc54'
    ],

    'not_keys': [
        '96f7acd 205a1487f305577be02ca861de1f8d1295c7b0e75e2292b8ba2e365db',
        '4cfaa06fdaa8f166af6fdd84b8e55270f7efc11cdb7f175c7eb0d9c85bebc54',
        '96f7acd205a1487f305577be02ca861de1fhd1295c7b0e75e2292b8ba2e365db',
        '96f7acd205a1487f305577be0,,a861de1f8d1295c7b0e75e2292b8ba2e365db'
    ]
}


class TestCrypto(object):

    def test_check_string(self):
        for _s in test_data['strings']:
            assert _check_string(_s)
        for _ns in test_data['not_strings']:
            assert not _check_string(_ns)

    def test_check_hex_string(self):
        for _s in test_data['hex_strings']:
            assert _check_hex_string(_s)
        for _ns in test_data['not_hex_strings']:
            assert not _check_hex_string(_ns)

    def test_check_utf8_string(self):
        for _s in test_data['utf8_strings']:
            assert check_utf8_string(_s)
        for _ns in test_data['not_utf8_strings']:
            assert not check_utf8_string(_ns)

    def test_check_pub_key(self):
        for _s in test_data['keys']:
            assert check_pub_key(_s)
        for _ns in test_data['not_keys']:
            assert not check_pub_key(_ns)

    def test_check_priv_key(self):
        for _s in test_data['keys']:
            assert check_priv_key(_s)
        for _ns in test_data['not_keys']:
            assert not check_priv_key(_ns)

    def test_generate_key_pair(self):
        for i in range(1000):
            _keys = generate_key_pair()
            assert check_pub_key(_keys['pub_key'])
            assert check_priv_key(_keys['priv_key'])

    def test_check_signature(self):
        for i in range(1000):
            for _message in test_data['utf8_strings']:
                _keys = generate_key_pair()
                _sig = sign_message(
                    message=_message,
                    priv_key=_keys['priv_key']
                )

                _sig_wrong = list(_sig)
                if _sig_wrong[34] == 'b':
                    _sig_wrong[34] = 'a'
                else:
                    _sig_wrong[34] = 'b'
                _sig_wrong1 = ''.join(_sig_wrong)

                _sig_wrong[100] = "k"
                _sig_wrong = ''.join(_sig_wrong)

                assert check_signature(signature=_sig)
                assert not check_signature(signature=_sig_wrong)
                assert validate_signed_message(pub_key=_keys['pub_key'], message=_message, signature=_sig)
                assert not validate_signed_message(pub_key=_keys['pub_key'], message=_message, signature=_sig_wrong1)
