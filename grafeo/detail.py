from .crypto import check_pub_key
import zbarlight
from PIL import Image


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
