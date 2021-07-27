"""Nicolò Sala, 18 luglio 2021"""

from argon2 import PasswordHasher   # type: ignore
from json import load, dump

USERS_FILE: str = "users.json"


def load_users() -> dict[str, str]:
    with open(USERS_FILE, "r") as f:
        return load(f)


def store_users() -> None:
    with open(USERS_FILE, "w") as f:
        dump(users, f, indent=4)


ph: PasswordHasher = PasswordHasher()
users: dict[str, str] = load_users()


def hash(password: str) -> str:
    return ph.hash(password)


def verify(password: str, digest: str) -> bool:
    return ph.verify(digest, password)


def valid_password(password: str) -> None:
    assert 16 <= len(
        password) <= 128, "The password length must be in range [16, 128]."
    assert all(map(str.isprintable, password)
               ), "All password characters must be printable."
    assert any(map(str.upper, password)
               ), "The password must contain at least one uppercase character."
    assert any(map(str.isdigit, password)
               ), "The password must contain at least one digit character."
    assert not all(map(str.isalnum, password)
                   ), "The password must contain at least one special character."


def valid_username(username: str) -> None:
    assert 1 <= len(
        username) <= 32, "The username length must be in range [1, 32]."
    assert username not in users, "There's already a user with the given username."


def register(username: str, password: str) -> None:
    valid_password(password)
    valid_username(username)
    users[username] = hash(password)


def login(username: str, password: str) -> None:
    assert username in users, "User not found."
    assert verify(password, users[username]), "The password is not correct."


if __name__ == "__main__":

    username: str = "hey"
    password: str = "Password1!"

    register(username, password)
    login(username, password)

    store_users()
