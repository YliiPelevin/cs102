def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for symbol in plaintext:
        if 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
            symbol_code = ord(symbol) + 3
            if symbol_code > ord('Z') and symbol_code < ord('a') or symbol_code > ord('z'):
                symbol_code -= 26
            ciphertext += chr(symbol_code)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for symbol in ciphertext:
        if 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
            symbol_code = ord(symbol) - 3
            if symbol_code > ord('Z') and symbol_code < ord('a') or symbol_code < ord('A'):
                symbol_code += 26
            plaintext += chr(symbol_code)
        else:
            plaintext += symbol

    return plaintext
