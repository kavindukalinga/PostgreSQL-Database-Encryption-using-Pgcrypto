import rsa

with open('sampleTXT.txt', 'rb') as f:
    data = f.read()

with open('private_key_file.pem', 'rb') as pr:
    private_key = rsa.PrivateKey.load_pkcs1(pr.read())

signature_file=rsa.sign(data, private_key, 'SHA-1')

# print(len(signature_file))   # 2048/8 = 256 bytes

with open('signature_file', 'wb') as sf:
    sf.write(signature_file)