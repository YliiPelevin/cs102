package caesar

func EncryptCaesar(plaintext string) string {
	ciphertext := ""
	for i := 0; i < len(plaintext); i++ {
		symbol := int(plaintext[i])
		if (int('A') <= symbol) && (symbol <= int('Z')) || (int('a') <= symbol && symbol <= int('z')) {
			symbol += 3
			if (symbol > int('Z') && symbol < int('a')) || symbol > int('z') {
				symbol -= 26
			}
			ciphertext += string(symbol)
		} else {
			ciphertext += string(plaintext[i])
		}
	}
	return ciphertext
}

func DecryptCaesar(ciphertext string) string {
	plaintext := ""
	for i := 0; i < len(ciphertext); i++ {
		symbol := int(ciphertext[i])
		if (int('A') <= symbol) && (symbol <= int('Z')) || (int('a') <= symbol && symbol <= int('z')) {
			symbol -= 3
			if (symbol > int('Z') && symbol < int('a')) || symbol < int('A') {
				symbol += 26
			}
			plaintext += string(symbol)
		} else {
			plaintext += string(ciphertext[i])
		}
	}
	return plaintext
}
