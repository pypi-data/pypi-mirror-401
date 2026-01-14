from enum import Enum


class Oauth2FlowType(str, Enum):
    IMPERSONATION = "IMPERSONATION"
    TEMPLATE = "TEMPLATE"
