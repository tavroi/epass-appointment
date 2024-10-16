from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

BLOCK_SIZE = AES.block_size

KEY=b'Y\xb9\x0b)\x89\xee\xf7\x07\xe6\xd6\x88\xe7\xb7B\x9d\xb6'
IV =b'Y\xb9\x0b)\x89\xee\xf7\x07\xe6\xd6\x88\xe7\xb7B\x9d\xb6'

def encrypt_base64_string(base64_string: str):
    """
    Encrypt a Base64 string using AES encryption.

    Args:
        base64_string (str): The Base64 string to encrypt.
        key (bytes): The AES key for encryption (optional, 128-bit key will be generated if not provided).
        iv (bytes): The initialization vector (IV) for AES (optional, 128-bit IV will be generated if not provided).

    Returns:
        tuple: A tuple containing the encrypted data, key, and IV.
    """
    # if key is None:
    #     key = get_random_bytes(16)  # 128-bit key
    # if iv is None:
    #     iv = get_random_bytes(16)   # 128-bit IV

    # Convert the Base64 string to bytes
    data_bytes = base64_string.encode('utf-8')
    
    # Encrypt the data bytes using AES
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted_data = cipher.encrypt(pad(data_bytes, BLOCK_SIZE))

    # Convert the encrypted data to a Base64 string
    encrypted_base64_string = base64.b64encode(encrypted_data).decode('utf-8')

    return encrypted_base64_string


def decrypt_to_base64_string(encrypted_base64_string: str) -> str:
    """
    Decrypt an encrypted Base64 string and return the original Base64 string.

    Args:
        encrypted_base64_string (str): The encrypted Base64 string to decrypt.
        key (bytes): The AES key used for encryption.
        iv (bytes): The initialization vector (IV) used for encryption.

    Returns:
        str: The decrypted original Base64 string.
    """
    # Convert the encrypted Base64 string to bytes
    encrypted_data = base64.b64decode(encrypted_base64_string.encode('utf-8'))

    # Decrypt the data bytes using AES
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_data), BLOCK_SIZE)

    # Convert the decrypted bytes back to the original Base64 string
    base64_string = decrypted_bytes.decode('utf-8')

    return base64_string

def encode_image_to_base64(image_bytes: bytes) -> str:
    """
    Encode image bytes to a Base64 string.

    Args:
        image_bytes (bytes): The image bytes to encode.

    Returns:
        str: The Base64 encoded string.
    """
    base64_string = base64.b64encode(image_bytes).decode('utf-8')
    return base64_string

def decode_base64_to_image(base64_string: str) -> bytes:
    """
    Decode a Base64 string back to image bytes.

    Args:
        base64_string (str): The Base64 encoded string to decode.

    Returns:
        bytes: The decoded image bytes.
    """
    image_bytes = base64.b64decode(base64_string.encode('utf-8'))
    return image_bytes
