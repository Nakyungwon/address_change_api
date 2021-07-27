import jwt
from django.conf import settings


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