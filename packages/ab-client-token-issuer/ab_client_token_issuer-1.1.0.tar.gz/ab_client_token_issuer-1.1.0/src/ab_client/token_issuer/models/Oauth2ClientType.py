from enum import Enum


class Oauth2ClientType(str, Enum):
    STANDARD = "STANDARD"
    PKCE = "PKCE"
