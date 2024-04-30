import rsa

public_key, private_key = rsa.newkeys(2048) # 256 bytes

with open('public_key_file.pem', 'wb') as puk:
    puk.write(public_key.save_pkcs1('PEM'))

with open('private_key_file.pem', 'wb') as prk:
    prk.write(private_key.save_pkcs1('PEM'))