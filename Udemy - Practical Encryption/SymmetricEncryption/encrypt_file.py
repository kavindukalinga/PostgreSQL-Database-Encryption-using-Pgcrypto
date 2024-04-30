from cryptography.fernet import Fernet

key = b'YCtLIyVrCsv6zQgRIvQ5dMDur4wj27OQlgxe6tj98Y8='

cipher = Fernet(key)


with open('YOURFILE', 'rb') as f:
    myfile = f.read()

edata = cipher.encrypt(myfile)  # save your encrypted file
with open('YOURFILE'+ ".encrypted", 'wb') as df:
    df.write(edata)


