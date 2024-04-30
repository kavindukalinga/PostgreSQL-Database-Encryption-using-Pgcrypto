import rsa

public_key, priv_key = rsa.newkeys(1024)  # generate pub & pri keys


def load_keys(filename):  # function to save keys to files
    with open(filename, 'wb')as f:
        if filename == 'public_key_file.pem':  # if we want a public key saved
            f.write(public_key.save_pkcs1('PEM'))  # format for saving keys
        elif filename == 'private_key_file.pem':
            f.write(priv_key.save_pkcs1('PEM'))


load_keys('public_key_file.pem')  # call load_keys function
load_keys('private_key_file.pem')
