import time
import hashlib
from TPlatform import settings


def data_sign():
    now_time = time.time()
    server_time = str(now_time).split(".")[0]
    md5 = hashlib.md5()
    sign_str = server_time + settings.SECRET_KEY
    sign_bytes_utf8 = str(sign_str).encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()
    return server_sign