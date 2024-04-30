import rsa

message = b' this is our text to hash'

htext = rsa.compute_hash(message,'SHA-512')

print(htext.hex())

message = b' this is our text to hash Im adding more text'

htext = rsa.compute_hash(message,'SHA-512')

print(htext.hex())
