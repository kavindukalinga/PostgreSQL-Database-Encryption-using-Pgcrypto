from cryptography.fernet import Fernet

key = b'YCtLIyVrCsv6zQgRIvQ5dMDur4wj27OQlgxe6tj98Y8='

cipher = Fernet(key)


with open('mytextfile.en','rb') as f:
    edata = f.read()

edata = cipher.decrypt(edata)  # save your encrypted file

with open('mytextfile.txt.decrypted', 'wb') as df:
    df.write(edata)
