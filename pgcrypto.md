# pgcrypto

<https://www.postgresql.org/docs/current/pgcrypto.html#PGCRYPTO-PGP-ENC-FUNCS>

## Symmetric key Encryption

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
drop table if exists cc;
CREATE TABLE cc (
    id SERIAL PRIMARY KEY,
    customer_id int,
    credit_card BYTEA
);
INSERT INTO cc(customer_id,credit_card) VALUES (2345,pgp_sym_encrypt('111122223333','encryption_password'));
INSERT INTO cc(customer_id,credit_card) VALUES (3456,pgp_sym_encrypt('222233334444','encryption_password'));
SELECT customer_id,credit_card,pgp_sym_decrypt(credit_card,'encryption_password') AS decrypted_data FROM cc where customer_id in (2345,3456);
SELECT customer_id,credit_card,pgp_sym_decrypt(credit_card,'wrong_password') AS decrypted_data FROM cc where customer_id in (2345,3456);
```

## Asymmetric key Encryption

### Generate key

```bash
root@022dd4a21793:/var/lib/postgresql/data/keys# gpg --default-new-key-algo rsa4096 --full-gen-key
gpg (GnuPG) 2.2.40; Copyright (C) 2022 g10 Code GmbH
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
  (14) Existing key from card
Your selection? 1
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 
Requested keysize is 3072 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 1y
Key expires at Fri 25 Apr 2025 06:47:52 AM UTC
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: kalinga
Email address: kavindukalingayu@gmail.com
Comment: For card
You selected this USER-ID:
    "kalinga (For card) <kavindukalingayu@gmail.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? o
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: /root/.gnupg/trustdb.gpg: trustdb created
gpg: directory '/root/.gnupg/openpgp-revocs.d' created
gpg: revocation certificate stored as '/root/.gnupg/openpgp-revocs.d/8E5B535902517F681BB8E355ED50ED22D9B57817.rev'
public and secret key created and signed.

pub   rsa3072 2024-04-25 [SC] [expires: 2025-04-25]
      8E5B535902517F681BB8E355ED50ED22D9B57817
uid                      kalinga (For card) <kavindukalingayu@gmail.com>
sub   rsa3072 2024-04-25 [E] [expires: 2025-04-25]

root@022dd4a21793:/var/lib/postgresql/data/keys# gpg -a --export 8E5B535902517F681BB8E355ED50ED22D9B57817 > ./public.key
root@022dd4a21793:/var/lib/postgresql/data/keys# gpg -a --export-secret-key 8E5B535902517F681BB8E355ED50ED22D9B57817 > ./private.key
# pssphrase = kalinga
root@022dd4a21793:/var/lib/postgresql/data/keys# ls
private.key  public.key
```

### Databse

```sql
INSERT INTO cc(customer_id,credit_card) VALUES (4567,pgp_pub_encrypt('333344445555',dearmor(pg_read_file('keys/public.key'))));
INSERT INTO cc(customer_id,credit_card) VALUES (5678,pgp_pub_encrypt('444455556666',dearmor(pg_read_file('keys/public.key'))));
SELECT customer_id,credit_card,pgp_pub_decrypt(credit_card,dearmor(pg_read_file('keys/private.key')),'kalinga') AS decrypted_data FROM cc where customer_id in (4567,5678);

```

## SQL Query to get data

```sql
DO $$
DECLARE
    private_key TEXT := '-----BEGIN PGP PRIVATE KEY BLOCK-----

lQWGBGYp/PIBDAC1xy8sC3v5TfvsVob4fVIvsIJVI1ebPdM1j23DHWckndv9YI0d
/RNwc/IzbvxLW6MyUrk0mN/mBx1GEKzExmx05zGVY864qgOtrnTWCi2vk+Cl8ykb
AV1uE4lW7ET4CVo9CwJWTk6W48ErmU7h6ww17+eQBZoSvBkg0wmLs+YA3IFH21rh
BBTtc+xh4lbqiI9yH9cGuljZOfhGwbXDVQyaXx6rl/0lkRDtqp6rBO0gaasYKUd5
3xCN9DfAfaeW26i/2+EUS2p6wxZsjc3Bebo4gG/Q5IF6OEIuIpFQtukECh7ygMYI
2kYqCQmvhL5gVi5nkzNlewewne3KBo/0Ck1rHkwCsy1v1tkft62OWA+oPgh/E4w3
qPRjJdh3ORKReXjGxPSIkNANyumkFPnLX7F8p5bfOQVDjI56yKcY852/SoPPcRRO
RBsgl6/MCekw1kRGY21OP2r6K6VHKbUqsgYQhQbXkxHt7hYhhWa/osPkITx2U7KB
2ioRoeqTYqnQW7cAEQEAAf4HAwIaKYlhYe6SZf+qTGR+XFk0YHUTK6gFKGKFb0XA
vWgS7WL4JjZYjBNaew1KrEN/ozorINLuNVqN+niBkxmR8s86iqyVBmZNCESB0UTC
UyIENv9+rpbGIoKgs8zbHZdqvqdB+piZ2357GHBKAwekOiyB/26laOBssXuvRpNq
R4bV8otlaeKrfARZ0Aj3uyAYWpM/NHiTOPfqvLRG0HB1344dSabmFKzpF9/dcGiS
pHbbrrxuoPQ0Vt1X5a8ehYhXLe6na4Me5AqYZ4wcTL5K7rAaCTEifZnE25dShgJm
z68BXZukMB4EucID/k46pocpZlSt2WMVTAYuOB0SwOGtcbsE7BjzXNsspWwypiOB
FE2x4LbKUBNrtVv69XsKrt+I+1dzp0l4h3iAyg34YC1q4IpShfo367ujIm1XrWOl
MJQcluzvPDgB2/qKU1Gz/vWEcPw83egkFxGGqMtYC2agIbQp5mTvHgtx2W7MfAmD
bZ3zLGGYoCxcjbozwjcSC6x+gOF4WmRwrCdHdFO6zYgE3GJwfO+CUY1TVPCEf5mH
1016056JN3Ey15C4npLKp71zL20qtNeA+s26diU1zIssVug3LIUZEhKT8s9TgLNp
X8EqDvVqIsJnE8Ghc4aXdnJ3vRkWYsMurPMGAj5yyZYCMnxUhDeocyfKRXQbvPb9
qWEFLqGwZGoeSi9dhWr6HELb7LXZ9vN9mnW4tckV9nUi+gSQqoFaJFE4XuolVe9A
n36yzX6bYPhBT62ajpOYoAgEqrZAzrToingnnuebgJKxFG6f4hRkYFN1DTY65MPd
vsi2/txRZUXAPGv5NVSeK6Qzsrncng2uXc0dhMY8uHQuhQF6+ThnKczV8yQndYNW
wfFLKPnhcwY4DbvvC6q67+V3LP9S3GRMf4oafppO8SN1ahr246vQFmbLy6lt8Uho
for52YtoxuEm/Z65iv9CvnmqcbZNg7cHzYw64ssV9rXmae3rOmorYxZTdaqIgsgG
MVhqkK80V/8aMA+XWNkF/v0s5Jh+y/EdKymBzaOvWrocLb+yZSuQkB+F4G0w7kKz
47FkTUNP1y3PzhqwJdV+jpMRFk07CsANJhrbCozTxbCrXfj6uEPp2QI/WqoONhhg
Q+hhpyroDui5cWj650vm5RVCms5RBBgNcV44KaNY2xdH0Ppt+hcQZ++wDjgVzS0B
ksnW0NV7cTWnd6QoFSG7FTJiliP3EAzo9kpyEQyqykwMIRDObMWx1k96QxcQR9gA
sOwnpco7YjhaIbgseZlEeK8PbXFjuC3wreUFm/Oq2jYBvRNaXW8kNv0NeFfo2pV3
kozmw0JeHn0Y3HrgFHFN7BfDngyMtg3RcbQva2FsaW5nYSAoRm9yIGNhcmQpIDxr
YXZpbmR1a2FsaW5nYXl1QGdtYWlsLmNvbT6JAdQEEwEKAD4WIQSOW1NZAlF/aBu4
41XtUO0i2bV4FwUCZin88gIbAwUJAeEzgAULCQgHAgYVCgkICwIEFgIDAQIeAQIX
gAAKCRDtUO0i2bV4F2pRC/9yJlwvNOmUFl0VZ9wFxqyJsmuMjK+Xf2YVm4iaSL/F
YDdeCJsgPEdZVR3yu7bregVbO8wFnO4e46Kdu0P3rSwUqM/YhhDYieqjuh2cJWwM
MjA6XDY+pnOC4+S6qZN04lQ60aBse/olKhKlh6vUcj51oLW13DO99YLbxawNt6yB
W7gNk5X00taDRy70b5lr6yOSfRujfvzquvMbyfcwi83R3YWIyAEp/jx8iSVr7YLB
4pD72Fcn1RpQwrxnnTW+KqlcHbYZ5opSZZS3z3kI3bEqw8xgw8yKjm4RW60nE9ea
uvfftVWFeBSjeiT9QwmrvOh2TvHD8jn5hmWZ5BkNMET9gqNdu3ClVND61xNjKEqS
zP7pqvR/wWGbHdoyHJoKDQNacv4TvgUHcD2l0kmjWOKic7oRIs6sviWDGjmA3ECZ
eNo2lcPYtDiB8b2IOQI9dtM6q/i27bBG0aH9jNEEZd2eVmE0HRNDe8/4dF3WhWNp
eQQz/3eoQP6xEC/RTbQ5zxGdBYYEZin88gEMAJwu+rLeaREDnTGzA/pPvJEp53V2
9ue/HWyPGTEyuEnOlDnHsYIfHn22lAcsT3UINYns3Oj0UJR+gg9fx9PTkAkZ6Bs3
VYCLctN6gv9/8bGfgRy7Gco3LQNwXj99hJsOqgSLqPdnv4tD2r3KYxwFPiGsk5ai
EGdhG6S3AR92dIFzArf4cYCre+j39ZqhqIA4tRSw6mtabV3205saTJ7y9MYkEjZU
jv+8Qc4j6rhYMQKlqlM8xzfLuK8Li55n05D474e8Sj52eWlrr72GwW+j674ztPOz
tv1+dWgr2xeDk+APrE5RAeyr4evze1wjb4o5mv0dGtJ+I+U3IyV4ZefHMxfuUBAW
hcGBya6yA6UmYk/uLQ5hQQrPgY95y0s7NlkpOJRNFDX34AkizJoGvwut6l0hZDkR
Hz+ptSOVEFQ8krNxRaJm+ZLkgOu6jSkqIfDFP+DFxGb0KmiCkQGP4YQ4AiU3Wq/0
sbWkC03xi5A7i1C5MRW+AlPY2D3l2r7OlM+1mwARAQAB/gcDAtvLTJxD3U4L//D9
XtdKVNzKZj2Bcx5+ZPvfjrC/0/aK6IqIBxVfvYNlJW5ZPcrVbsTq15VDFlJii9UL
bgmFOMDlmduiWRsFbpBejJl2bTD3+7lelT4rDLPUkqCyWJw+oEOcwFTIoWl3VIX/
BKsE3En3hLicMeKSDhv3XaZscSRyAKsNe5AEICq+WTD6LWmXJJZ+sCMABm1LYGD/
pLvrqZ2pjhCnZF8W6cydJFQT+YvU9K+/6Y3rAr6rX/eXLn9oiV7U4eMfhXKyFVHZ
79ZRKJqFZFk3nQl/qjHEFG/ITCdmZXK9ZiNEHByGA8swC8/T3XNhWZ+G0scpRX3d
LPiXU6AA2VoTMeTMDoEBs+vBFdQaeHCsf4fO2YNfa06TYJsMvcTMkJxf2Rr53zA/
Htez/Z4KXqHlnFZeH22g/HSmbiTesQTUcJwxWQ4bKbf1GD0TUGyCKB3bkXHOoK9d
2NIq6sP8Tyc6CMbWb3evUnoQF+pEce7NgDf9D3W2dx66/6b6XzOXoVoTE0xe6mnj
SHd+vlteaae5EPTp2bVXLMy44l3h2225xZr/WFS+46qtdiaWBuMlJOFg+sAgo3pS
FQwnfLMeCUSD+VGh9Mi3Jzo+6sAt39QapMSD/Q2fEAh4Hg4Gm77rxjhgxzK1thUW
cuQ+Q07g8idIr3BAOSn8lUvy0XGjnW5aXpGeRD7w1130WQxkbDzR4nHdqEHBMjHV
IXnJ9G7CSJyiIUNUKhXcfAuJP8qnmxkDIBx+oGF4YjpdbTlyUDbP9H2mWZwk/beF
4Sne6N8PHjgflCzfcb/IdifTCwIaoSFScSDp1lbtDA3bJ8UAkLi+sVKbm/S9WLRi
j6SwvQTEJLTHvxC4d9Qab5n+X19dRX1kkPIcthWGczma4FN6jxaAMsb/Mz1hZqST
pHdpDXcstawnCE0bS00lHhOE24/VHkFb3tYX2SlSfiZ3UVVu1aStS7qTtyoHepMw
dAYDgUtRZw+S9b77Y+JxgMatB750hLg7bVmjluv7bTIj59VU+RHPDdkv8t81oaMz
xUkIvV77gwK8XgRVYKMFXiVlTLveV2jsxfPpkmbOc7u5Yec+MD+giC3fjk1yHEvf
H+tskU7wZ9bVWcBbr8FAeFKoJMM6qNEI/sefGaVAZW4iJB4rby0YdPbG9aIuqRgf
BfYc1D4YKUNAA5ZUUMZrnxatcUUOc02bZLR4I/Sr2mTKS9qLo1eBpqWSDzqL7/mG
Wts/hOdhyw5Xt4SOqj3hGWd8fRsNWWHyR0B8hxy/iI1YpaeDdKPn8kFnfGUDl+3a
kYEDjBAQENtpjAbwTjPnJ1iPWhofKK8eQm0Ctj0DCg8dzwCXmJqJ5WrNiQG8BBgB
CgAmFiEEjltTWQJRf2gbuONV7VDtItm1eBcFAmYp/PICGwwFCQHhM4AACgkQ7VDt
Itm1eBe7EwwAs5F8fRlgyTClILHe0OIkCL6a2/7LFDqTF800EmYaoVZ1k5pu4ZhV
gxrdde66e7g9oWk49tnyd7MedNU/eAfAv9NQR5/LwUywv8eU9iFTNXcfLy6bockM
lKOCOWaK62gsmchowEeOPgufVa4rLAevl8rXyqP85gf//4xiYge47gNBSkhEcXW4
hgttkSNvnpktRjxBjw/srIhRP7Ccf809fbc9aujBOvYR1kpmRuyfWv/JssUj+8Zq
XkkkziJOo4tTog9d5kI6K9/WmN2u7F/r4quSA50ufT7cP7TWK/YVlJiEi5RhJie4
bF6bkxAEa8zoDBJHt68ua+CsNLggcGwDEuEelvH7sCeLtzv10qXihQm4WlMJOyah
JDh1PbIO2j5/wU/HD3qqn0eocdeETH9c8PHfpNCTVcEiuN8V9ifTx627SZzl28Th
s//fNqaUOED5AhEjJrSP9h1S3FSudKUmiXn6831bEHuQuDgWOdnTtYAm+zqxcZO4
hjWUEKCutOWd
=IA1M
-----END PGP PRIVATE KEY BLOCK-----';
BEGIN
    DROP TABLE IF EXISTS decrypted_data; -- Drop the table if it already exists
    CREATE TEMP TABLE decrypted_data AS
    SELECT
		id,
        customer_id,
        pgp_pub_decrypt(credit_card, dearmor(private_key), 'kalinga') AS decrypted_credit_card
    FROM
        public.cc;
END $$;
SELECT * FROM decrypted_data;

```


## Logs

```sql
SELECT query, calls rows FROM pg_stat_statements;

```

## Steps

```bash
sudo apt update && sudo apt upgrade gnupg
gpg --import ./keys/private.key 
python3 decrypt-data.py
```
