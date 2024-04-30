from cryptography.fernet import Fernet

key = Fernet.generate_key() # generate the key
print(key)

cipher = Fernet(key) # incorporate the key with the cipher

encrypted_text = cipher.encrypt(b'this is my secret') # encrypt the string

print(encrypted_text)


decrypted_text = cipher.decrypt(encrypted_text)
print(decrypted_text.decode())

