from passlib.context import CryptContext 
#if you use bcrypt algo for Hashing use this and change bcrypt in schemes bcrypt is hashing slower but safe
# from argon2 import PasswordHasher 
# from argon2.exceptions import VerifyMismatchError, InvalidHash  
#these bothline use for argon2 algo this is used in modern tech it hashing the password more fast and also secure

pass_context=CryptContext(schemes=["bcrypt"], deprecated="auto")  #schemes=["argon2"]

def hash(pass_word: str):
    # pass_word = pass_word.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pass_context.hash(pass_word)

 #to login check the password is matched or not    
def verify(p_password:str, h_password:str):
    return pass_context.verify(p_password, h_password)  