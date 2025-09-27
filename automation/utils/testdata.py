from __future__ import annotations
from dataclasses import dataclass

@dataclass
class UserCreds:
    username: str
    password: str

DEFAULT_VALID = UserCreds("standard_user", "secret_sauce")
NEGATIVE_LOCKED = UserCreds("locked_out_user", "secret_sauce")
NEGATIVE_WRONGPASS = UserCreds("standard_user", "wrong_password")

@dataclass
class Person:
    first: str
    last: str
    postal: str

DEFAULT_PERSON = Person("Jane", "Doe", "12345")
