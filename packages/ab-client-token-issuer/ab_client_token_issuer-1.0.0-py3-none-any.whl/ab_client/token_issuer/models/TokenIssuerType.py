from enum import Enum


class TokenIssuerType(str, Enum):
    PKCE = "PKCE"
    OAUTH2 = "OAUTH2"
    TEMPLATE = "TEMPLATE"
