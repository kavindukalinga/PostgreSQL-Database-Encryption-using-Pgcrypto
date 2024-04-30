import rsa

paul_pub, paul_priv = rsa.newkeys(1024)

e_data = rsa.encrypt(b'this is my secret message', paul_pub)

print(e_data)

d_data = rsa.decrypt(e_data,paul_priv)

print(d_data.decode())