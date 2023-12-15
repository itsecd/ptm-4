from cryptography.fernet import Fernet
from sys import getdefaultencoding

def main(text:str)->bytes:
    getdefaultencoding()
    
    cipher_key = Fernet.generate_key()
    cipher = Fernet(cipher_key)
    
    
    encrypted_text = str(cipher.encrypt(text.encode()))
    
    encrypted_text = encrypted_text[2:-1:1]
    cipher_key = str(cipher_key)[2:-1:1]
    
    return encrypted_text, cipher_key