from __future__ import annotations

import hashlib
import json
import zlib
from datetime import datetime
from typing import Any, Final

import httpx
import pytz  # type: ignore[import-untyped]
from Crypto.Cipher import AES  # type: ignore[import-not-found]
from Crypto.Util.Padding import unpad  # type: ignore[import-not-found]

AesKey: Final[str] = "n7bx6:@Fg_:2;5E89Phy7AyIcpxEQ:R@"
AesIV: Final[str] = ";;KjR1C3hgB1ovXa"
ObfuscateParam: Final[str] = "BEs2D5vW"
KeychipID: Final[str] = "A63E-01C28055905"

_SDGB_ENDPOINT: Final[str] = "https://maimai-gm.wahlap.com:42081/Maimai2Servlet/"


class aes_pkcs7(object):
    def __init__(self, key: str, iv: str) -> None:
        self.key = key.encode("utf-8")
        self.iv = iv.encode("utf-8")
        self.mode = AES.MODE_CBC

    def encrypt(self, content: str) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        content_padding = self.pkcs7padding(content)
        encrypt_bytes = cipher.encrypt(content_padding.encode("utf-8"))
        return encrypt_bytes

    def decrypt(self, content: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.decrypt(content)

    def pkcs7unpadding(self, text: str) -> str:
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0 : length - unpadding]

    def pkcs7padding(self, text: str) -> str:
        bs = 16
        length = len(text)
        bytes_length = len(text.encode("utf-8"))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        return text + padding_text


def get_hash_api(api: str) -> str:
    return hashlib.md5((api + "MaimaiChn" + ObfuscateParam).encode()).hexdigest()


async def sdgb_api(
    data: str,
    use_api: str,
    user_id: int,
    *,
    client: httpx.AsyncClient | None = None,
) -> str:
    aes = aes_pkcs7(AesKey, AesIV)
    data_enc = aes.encrypt(data)
    data_def = zlib.compress(data_enc)

    url = _SDGB_ENDPOINT + get_hash_api(use_api)
    headers: dict[str, str] = {
        "User-Agent": f"{get_hash_api(use_api)}#{user_id}",
        "Content-Type": "application/json",
        "Mai-Encoding": "1.40",
        "Accept-Encoding": "",
        "Charset": "UTF-8",
        "Content-Encoding": "deflate",
        "Expect": "100-continue",
    }

    if client is None:
        async with httpx.AsyncClient(timeout=20.0) as created_client:
            resp = await created_client.post(url, headers=headers, content=data_def)
    else:
        resp = await client.post(url, headers=headers, content=data_def)

    resp.raise_for_status()
    resp_def = resp.content

    try:
        resp_enc = zlib.decompress(resp_def)
    except zlib.error:
        resp_enc = resp_def

    return unpad(aes.decrypt(resp_enc), 16).decode()


async def qr_api(qr_code: str, *, client: httpx.AsyncClient | None = None) -> dict[str, Any]:
    if len(qr_code) > 64:
        qr_code = qr_code[-64:]
    time_stamp = datetime.now(pytz.timezone("Asia/Tokyo")).strftime("%y%m%d%H%M%S")
    auth_key = hashlib.sha256(
        (KeychipID + time_stamp + "XcW5FW4cPArBXEk4vzKz3CIrMuA5EVVW").encode("UTF-8")
    ).hexdigest().upper()
    param: dict[str, str] = {
        "chipID": KeychipID,
        "openGameID": "MAID",
        "key": auth_key,
        "qrCode": qr_code,
        "timestamp": time_stamp,
    }
    headers: dict[str, str] = {
        "Contention": "Keep-Alive",
        "Host": "ai.sys-all.cn",
        "User-Agent": "WC_AIME_LIB",
    }

    url = "http://ai.sys-allnet.cn/wc_aime/api/get_data"
    body = json.dumps(param, separators=(",", ":"))

    if client is None:
        async with httpx.AsyncClient(timeout=20.0) as created_client:
            res = await created_client.post(url, content=body, headers=headers)
    else:
        res = await client.post(url, content=body, headers=headers)

    res.raise_for_status()
    return json.loads(res.content)
