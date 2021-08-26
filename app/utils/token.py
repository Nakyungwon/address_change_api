import jwt
from django.conf import settings

import base64
from Crypto import Random
from Crypto.Cipher import AES


class JWTToken:
    jwt_secret_key = getattr(settings, 'JWT_SECRET_KEY', None)
    algorithm = getattr(settings, 'ALGORITHM', None)
    
    @classmethod
    def encodeToken(cls, target):
        encoded_token = jwt.encode(target, cls.jwt_secret_key, algorithm=cls.algorithm)
        return encoded_token

    @classmethod
    def decodeToken(cls, encoded_token):
        try:
            decoded_token = jwt.decode(encoded_token, options={"verify_signature": False})
            return decoded_token
        except jwt.exceptions.DecodeError:
            print('decode error')


class AES128Crypto:

    def __init__(self):
        self.BS = AES.block_size
        # 암호화 키중 16자리만 잘라서 쓴다.
        encrypt_key = getattr(settings, 'CRYPTO_KEY', None)
        self.encrypt_key = encrypt_key[:16].encode(encoding='utf-8', errors='strict')
        self.pad = lambda s: bytes(s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS), 'utf-8')
        self.unpad = lambda s: s[0:-ord(s[-1:])]

    def encrypt(self, raw):
        raw = self.pad(raw)
        # initialization vector 를 매번 랜덤으로 생성 한다.
        iv = Random.new().read(self.BS)
        cipher = AES.new(self.encrypt_key, AES.MODE_CBC, iv)

        # 암호화시 앞에 iv와 암화화 값을 붙여 인코딩 한다.
        # 디코딩시 앞에서 BS(block_size) 만금 잘라서 iv를 구하고, 이를통해 복호화 한다.
        return base64.b64encode(iv + cipher.encrypt(raw)).decode("utf-8")

    def decrypt(self, enc):
        enc = base64.b64decode(enc)

        # encrypt 에서 작업한 것처럼 첫 16바이트(block_size=BS) 를 잘라 iv를 만들고, 그 뒤를 복호화 하고자 하는 메세지로 잘라 만든다.
        iv = enc[:self.BS]
        encrypted_msg = enc[self.BS:]
        cipher = AES.new(self.encrypt_key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(encrypted_msg)).decode('utf-8')
