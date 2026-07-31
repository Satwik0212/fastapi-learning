from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #this is for hashing the password

def hash(password: str) :
    return pwd.context.hash(password)