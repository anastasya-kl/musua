from datetime import datetime
import hashlib

def convert_into_date(date):
    try:
        converted_date = datetime.strptime(date, '%Y-%m-%d').date()
        return converted_date.strftime('%Y-%m-%d')
    except ValueError:
        return None
    

def hash_password(password):
    if len(password) > 20:
        raise ValueError("Password must be 20 characters or less")

    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()

    return hashed_password[:20]
    