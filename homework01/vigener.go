package vigener

func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string

	// PUT YOUR CODE HERE
	var sdvig int
	ciphertext = ""
	for i := 0; i < len(plaintext); i++ {
		symbol := int(plaintext[i])
		if (int('A') <= symbol) && (symbol <= int('Z')) || (int('a') <= symbol && symbol <= int('z')) {
			sdvig = int(keyword[i%len(keyword)])
			if (int('z') >= symbol) && (symbol >= int('a')) {
				sdvig -= int('a')
			} else {
				sdvig -= int('A')
			}

			symbol_code := symbol + sdvig
			if (int('a') <= symbol && symbol <= int('z')) && (symbol_code > int('z')) {
				symbol_code -= 26
			} else if int('A') <= symbol && symbol <= int('Z') && symbol_code > int('Z') {
				symbol_code -= 26
			}
			ciphertext += string(symbol_code)
		} else {
			ciphertext += string(symbol)
		}
	}

	return ciphertext
}

func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string

	// PUT YOUR CODE HERE
	var sdvig int
	plaintext = ""
	for i := 0; i < len(ciphertext); i++ {
		symbol := int(ciphertext[i])
		if (int('A') <= symbol) && (symbol <= int('Z')) || (int('a') <= symbol && symbol <= int('z')) {
			sdvig = int(keyword[i%len(keyword)])
			if (int('z') >= symbol) && (symbol >= int('a')) {
				sdvig -= int('a')
			} else {
				sdvig -= int('A')
			}
			symbol_code := symbol - sdvig
			if (int('a') <= symbol && symbol <= int('z')) && (symbol_code < int('a')) {
				symbol_code += 26
			} else if int('A') <= symbol && symbol <= int('Z') && symbol_code < int('A') {
				symbol_code += 26
			}
			plaintext += string(symbol_code)
		} else {
			plaintext += string(symbol)
		}
	}

	return plaintext
}
