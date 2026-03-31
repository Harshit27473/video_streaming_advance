import base64
import hashlib
import hmac

def get_secret_hash(username: str, client_id: str, client_secret: str):
    message= username + client_id

    digest = hmac.new(
        client_secret.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256,
    
    ).digest()

    return base64.b64encode(digest).decode()