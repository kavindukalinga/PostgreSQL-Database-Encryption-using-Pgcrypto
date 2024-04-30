# RSA

## Key-pair

```bash
pip install rsa
```

```python
import rsa
public,private = rsa.newkeys(1028)
print(private.save_pkcs1('PEM').decode())
#         -----BEGIN RSA PUBLIC KEY-----
#         MIGJAoGBCP16uxeUjHkVskjpa20e1trmVIiVh+bhnDw4VeV4yUTIS4BBESSaLYNC
#         22EDTL0o3xVxEtr85M0HV9fP5iGsVSidh/mTsyHrFhWPaZfUS/m0jce8aXvtEFYo
#         MbaBgdkWqFbKfol5fGyx+AdFCMU4loaxw/lNEhy/WhC51130yXi/AgMBAAE=
#         -----END RSA PUBLIC KEY-----
```
