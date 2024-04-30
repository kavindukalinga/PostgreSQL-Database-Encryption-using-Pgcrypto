from cryptography.fernet import Fernet
import rsa

key = Fernet.generate_key()  # create the random symmetric keys
cipher = Fernet(key)  # create the symmetric cipher

with open('public_key_file.pem', 'rb') as pk:  # open the pub key file and read in the pub key
    pub_key = rsa.PublicKey.load_pkcs1(pk.read())  # format for loading in keys
    encrypt_symmetric_key = rsa.encrypt(key, pub_key)  # encrypt the symmetric key with the pub key

with open('Word.docx', 'rb') as wf:  # open and encrypt Word file
    encrypted_word = cipher.encrypt(wf.read())

with open('encrypted_file', 'wb') as ef:  # open new file to save key and encrypted word doc
    ef.write(encrypt_symmetric_key)
    ef.write(encrypted_word)
