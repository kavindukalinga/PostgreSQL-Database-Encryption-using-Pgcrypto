import rsa
from cryptography.fernet import Fernet

# open the private key file and read in private key
with open('private_key_file.pem','rb') as pkey:
    priv_key = rsa.PrivateKey.load_pkcs1(pkey.read())

# open the encrypted file and read in key & file
with open('encrypted_file','rb') as ef:
    efile = ef.read(128)
    efWord = ef.read()

decrypted_key = rsa.decrypt(efile,priv_key) # decrypt asymmetric key
cipher = Fernet(decrypted_key) # create the cipher
decrypted_file = cipher.decrypt(efWord) # decrypt the Word file

with open('decrypted_word.docx','wb') as org: # save the decrypted file back to word format
    org.write(decrypted_file)

