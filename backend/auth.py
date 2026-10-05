USERNAME = "admin"
PASSWORD = "1234"


def login(username, password):
    if username == USERNAME and password == PASSWORD:
        return True

    return False