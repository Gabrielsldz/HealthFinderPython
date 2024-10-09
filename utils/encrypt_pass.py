import bcrypt


def encrypt_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password: str, password:str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

