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

Real name: yourName
Email address: <youremail@yomail.com>
Comment: For card
You selected this USER-ID:
    "yourName (For card) <youremail@yomail.com>"

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
uid                      yourName (For card) <youremail@yomail.com>
sub   rsa3072 2024-04-25 [E] [expires: 2025-04-25]

root@022dd4a21793:/var/lib/postgresql/data/keys# gpg -a --export 8E5B535902517F681BB8E355ED50ED22D9B57817 > ./public.key
root@022dd4a21793:/var/lib/postgresql/data/keys# gpg -a --export-secret-key 8E5B535902517F681BB8E355ED50ED22D9B57817 > ./private.key
# pssphrase = yourPassphrase
root@022dd4a21793:/var/lib/postgresql/data/keys# ls
private.key  public.key
```

### Databse

```sql
INSERT INTO cc(customer_id,credit_card) VALUES (4567,pgp_pub_encrypt('333344445555',dearmor(pg_read_file('keys/public.key'))));
INSERT INTO cc(customer_id,credit_card) VALUES (5678,pgp_pub_encrypt('444455556666',dearmor(pg_read_file('keys/public.key'))));
SELECT customer_id,credit_card,pgp_pub_decrypt(credit_card,dearmor(pg_read_file('keys/private.key')),'yourPassphrase') AS decrypted_data FROM cc where customer_id in (4567,5678);

```

## SQL Query to get data

```sql
DO $$
DECLARE
    private_key TEXT := '-----BEGIN PGP PRIVATE KEY BLOCK-----
lQWGBGYp/PIBDAC1xy8sC3v5TfvsVob4fVIvsIJVI1ebPdM1j23DHWckndv9YI0d
////////////////<YOUR FULL PRIVATE KEY>/////////////////////////
qsOCOWaK62gsmchowEeOPgufVa4rLAevl8rXyqP85gf//4xiYge47gNBSkhEcXW4
=IA1M
-----END PGP PRIVATE KEY BLOCK-----';
BEGIN
    DROP TABLE IF EXISTS decrypted_data; -- Drop the table if it already exists
    CREATE TEMP TABLE decrypted_data AS
    SELECT
		id,
        customer_id,
        pgp_pub_decrypt(credit_card, dearmor(private_key), 'yourPassphrase') AS decrypted_credit_card
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
