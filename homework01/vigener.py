def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for num, symbol in enumerate(plaintext):
        if 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
            shift = ord(keyword[num % len(keyword)])
            shift -= ord('a') if 'z' >= symbol >= 'a' else ord('A')
            symbol_code = ord(symbol) + shift
            if 'a' <= symbol <= 'z' and symbol_code > ord('z'):
                symbol_code -= 26
            elif 'A' <= symbol <= 'Z' and symbol_code > ord('Z'):
                symbol_code -= 26
            ciphertext += chr(symbol_code)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for num, symbol in enumerate(ciphertext):
        if 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
            shift = ord(keyword[num % len(keyword)])
            shift -= ord('a') if 'z' >= symbol >= 'a' else ord('A')
            symbol_code = ord(symbol) - shift
            if 'a' <= symbol <= 'z' and symbol_code < ord('a'):
                symbol_code += 26
            elif 'A' <= symbol <= 'Z' and symbol_code < ord('A'):
                symbol_code += 26
            plaintext += chr(symbol_code)
        else:
            plaintext += symbol
    return plaintext
