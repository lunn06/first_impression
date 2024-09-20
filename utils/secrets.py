from __future__ import annotations

import os
import base64
from hashlib import sha256


import qrcode  # type: ignore
from pyotp import TOTP


class Secret:
    name: str
    secret: str
    totp: TOTP

    DIR = os.getcwd() + os.sep + "secrets"

    def __init__(self, name: str, interval: int = 30, secret: str | None = None):
        self.secret = name if secret is None else secret
        self.name = name
        self.totp = self._generate_secret(interval)

    def verify(self, code: str) -> bool:
        return self.totp.verify(code)

    def _generate_secret(self, interval: int) -> TOTP:
        base = base64.b32encode(self.secret.encode())
        totp = TOTP(base.decode(), interval=interval)
        uri = totp.provisioning_uri(name=self.name, issuer_name="День программиста")

        if not os.path.exists(Secret.DIR):
            os.makedirs(Secret.DIR)

        qrcode.make(uri).save(f"{Secret.DIR}{os.sep}{self.name}.png")

        return totp
