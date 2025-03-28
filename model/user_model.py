from dataclasses import dataclass


@dataclass
class User:
    username: str
    email: str
    phone: str
    age: int

#TODO: Add UnregisteredUser model
