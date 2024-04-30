import rsa

with open('sampleTXT.txt', 'rb') as f:
    data = f.read()

with open('public_key_file.pem', 'rb') as puk:
    public_key = rsa.PublicKey.load_pkcs1(puk.read())

with open('signature_file', 'rb') as sf:
    signature_file = sf.read()

try:
    verify_file=rsa.verify(data, signature_file, public_key)

    print(verify_file)
except:
    print('Verification failed')
