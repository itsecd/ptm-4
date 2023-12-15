from cryptography.fernet import Fernet
from sys import getdefaultencoding
from base64 import urlsafe_b64encode

def DecodeText(text: bytes, key:bytes) -> str:
    
    getdefaultencoding()
    
    cipher = Fernet(key)
    
    decrypted_text = cipher.decrypt(text)
    
    return decrypted_text.decode("utf-8")