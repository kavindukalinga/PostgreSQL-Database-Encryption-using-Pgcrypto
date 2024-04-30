# PostgreSQL Database Encryption using Pgcrypto

- Project: How to encrypt data in PostgreSQL database in server using `pgcrypto`. Here a sensitive data column in a Database Table is encrypted using symmetric and as well as asymmetric encryption.
- Author: Kavindu Kalinga
- Databse: `postgreSQL`
- Tools: `gnupg` , `pgcrypto`, `PGAdmin4` , `FlaskAPI`
- Concepts used: `Symmetric Encryption` , `Asymmetric Encryption` , `RSA` 
- Languages: `python3`
- Containerization tools and APIs: `Docker`, `docker-compose`

## Content
- [PostgreSQL Database Encryption using Pgcrypto](#postgresql-database-encryption-using-pgcrypto)
  - [Content](#content)
  - [Database Init](#database-init)
    - [Useful Commands](#useful-commands)
  - [Symmetric key Encryption](#symmetric-key-encryption)
    - [PGcrypto init](#pgcrypto-init)
    - [Table init with encrypted column "credit\_card"](#table-init-with-encrypted-column-credit_card)
    - [Data Encryption](#data-encryption)
    - [Data Decryption](#data-decryption)
  - [Asymmetric key Encryption](#asymmetric-key-encryption)
    - [Generate key](#generate-key)
    - [PGcrypto init](#pgcrypto-init-1)
    - [Table init with encrypted column "credit\_card"](#table-init-with-encrypted-column-credit_card-1)
    - [Data Encryption](#data-encryption-1)
    - [Data Decryption](#data-decryption-1)
  - [View Data](#view-data)
    - [Without Private.key](#without-privatekey)
    - [With Private.key](#with-privatekey)
  - [Access Data](#access-data)
    - [API with private key](#api-with-private-key)
    - [Get data and decrypt locally](#get-data-and-decrypt-locally)
  - [Logs](#logs)
    - [pg stat statements](#pg-stat-statements)
    - [Enable logs](#enable-logs)
    - [View Logs](#view-logs)
  - [Contributors](#contributors)

## Database Init

Here using `docker-compose`, the database can be initiated. The configuration is defined in `docker-compose.yml`.

```bash
docker compose up
+++++++++++++++++++
docker compose down
```

Then using PGAdmin4 (or similar software), the database can be viewed and queried.

### Useful Commands

```bash
# Exec into container
docker exec -it pgdb4 bash

# Access Database
psql -n postgres -U postgres

# List databases
\l

# Change database to testdb
\c testdb

# List tables
\dt
```

## Symmetric key Encryption

### PGcrypto init

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

### Table init with encrypted column "credit_card"

```sql
drop table if exists cc;
CREATE TABLE cc (
    id SERIAL PRIMARY KEY,
    customer_id int,
    credit_card BYTEA
);
```

### Data Encryption

```sql
INSERT INTO cc(customer_id,credit_card) VALUES (2345,pgp_sym_encrypt('111122223333','encryption_password'));
INSERT INTO cc(customer_id,credit_card) VALUES (3456,pgp_sym_encrypt('222233334444','encryption_password'));
```

### Data Decryption

```sql
SELECT customer_id,credit_card,pgp_sym_decrypt(credit_card,'encryption_password') AS decrypted_data FROM cc where customer_id in (2345,3456);
SELECT customer_id,credit_card,pgp_sym_decrypt(credit_card,'wrong_password') AS decrypted_data FROM cc where customer_id in (2345,3456);
```

## Asymmetric key Encryption

### Generate key

```bash
# In the databse container
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

### PGcrypto init

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

### Table init with encrypted column "credit_card"

```sql
drop table if exists cc;
CREATE TABLE cc (
    id SERIAL PRIMARY KEY,
    customer_id int,
    credit_card BYTEA
);
```

### Data Encryption

```sql
INSERT INTO cc(customer_id,credit_card) VALUES (4567,pgp_pub_encrypt('333344445555',dearmor(pg_read_file('keys/public.key'))));
INSERT INTO cc(customer_id,credit_card) VALUES (5678,pgp_pub_encrypt('444455556666',dearmor(pg_read_file('keys/public.key'))));
```

### Data Decryption

```sql
SELECT customer_id,credit_card,pgp_pub_decrypt(credit_card,dearmor(pg_read_file('keys/private.key')),'yourPassphrase') AS decrypted_data FROM cc where customer_id in (4567,5678);
```

## View Data

The private key in server `keys/private.key` should be removed, otherwise anyone who has access to the server can get the key. But public key `keys/public.key` is always there to encrypt data.

### Without Private.key

Without the private.key, the encrypted data can not be decrypted.

```sql
SELECT * FROM public.cc
```

![PgAdmin Encrypted](Img/pgAdmin%20encrypted.png)

Here only the encrypted data can be seen.

### With Private.key

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

![PgAdmin Decrypted](Img/PgAdmin%20decrypted.png)
Here with the private.key, the decrypted data can be seen.

## Access Data

When accessing and viewing data using the `private.key`, the main issue is that anyone who has access to the server can inspect logs (/postgres logs) and get the key from the logs (When someone query using `private.key`, the logs record the query and query contains the key)  

> For more clarifications, go view the [View Logs](#view-logs)

### API with private key

Here `api.py` is written using Flask and can be accessed using `localhost:5000`.

```bash
python3 api.py
```

> In the API, first it reads the `private.key` and using that, it query the database and get the decrypted data directly.
> Therefore the data is decrypted inside the database server.
> The logs record the query and query contains the `private.key`

![API to Access Data](Img/Access%20Using%20api.png)

In the API, using `/store_data/<int:customer_id>/<string:credit_card>` , data can be stored in the database and using `/get-data`, data can be viewed.

### Get data and decrypt locally

Here what `decrypt-data.py` does is just query the encrypted data into the local machine and then the encrypted data is decrypted using the `private.key` locally.

```bash
python3 decrypt-data.py
```

> Here in this script, first load the encrypted data and the data is decrypted locally. Not in the database server.
> The logs do not record any sensitive data like `private.key`

But first the `private.key` should be configured using `GnuPG` in the local machine.

```bash
sudo apt update && sudo apt upgrade gnupg
gpg --import ./keys/private.key 
```

![API to Access Data](Img/Access%20data%20using%20decrypt-data.png)

Here in this example,
- First it can not decrypt data without the `passphrase`
- After adding the `passphrase`, now the script can decrypt the data without an issue.

## Logs

### pg stat statements

```sql
SELECT query, calls rows FROM pg_stat_statements;
```

### Enable logs

To Enable logs, `/var/lib/postgresql/data/postgresql.conf` configuration file should be changed as follows.

```conf
# -----------------------------
# Logging Parameters
# -----------------------------

# Where to log
log_destination = 'stderr' # Log to standard error output

# Verbosity for logging (change as needed)
log_statement = 'all'          # Log all SQL statements
log_min_duration_statement = 0 # Log all statements that run for more than 0 milliseconds (adjust as needed)

# These settings specify what to log regarding connections
log_connections = on    # Log connections
log_disconnections = on # Log disconnections

# These settings specify what to log regarding errors and messages
logging_collector = on          # Enable log collection
log_directory = 'pg_log'        # Directory where log files will be stored
log_filename = 'postgresql.log' # Prefix of log file names
log_file_mode = 0600            # Permissions for log files

# Adjust the following settings according to your needs
log_rotation_age = 1d    # Rotate logs daily
log_rotation_size = 10MB # Rotate logs when they reach 10MB

# Other parameters you may want to adjust
# log_lock_waits = on  # Log lock waits
# log_temp_files = 0  # Log temporary file usage

# -----------------------------
# End of Logging Parameters
# -----------------------------
```

### View Logs

1. Logs When connecting to server

```log
2024-04-30 07:51:04.861 UTC [1] LOG:  starting PostgreSQL 16.2 (Debian 16.2-1.pgdg120+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
2024-04-30 07:51:04.861 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2024-04-30 07:51:04.861 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2024-04-30 07:51:04.862 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2024-04-30 07:51:04.864 UTC [31] LOG:  database system was shut down at 2024-04-30 07:50:59 UTC
2024-04-30 07:51:04.867 UTC [1] LOG:  database system is ready to accept connections
```

2. Logs when data is accessed using SQLquery with the `private.key` included

```log
2024-04-30 07:52:01.096 UTC [45] LOG:  connection received: host=172.21.0.1 port=60608
2024-04-30 07:52:01.098 UTC [45] LOG:  connection authenticated: identity="postgres" method=scram-sha-256 (/var/lib/postgresql/data/pg_hba.conf:128)
2024-04-30 07:52:01.098 UTC [45] LOG:  connection authorized: user=postgres database=testdb
2024-04-30 07:52:01.099 UTC [45] LOG:  statement: BEGIN
2024-04-30 07:52:01.099 UTC [45] LOG:  duration: 0.075 ms
2024-04-30 07:52:01.099 UTC [45] LOG:  statement: SELECT customer_id, pgp_pub_decrypt(credit_card, dearmor('-----BEGIN PGP PRIVATE KEY BLOCK-----
	
	lQWGBGYp/PIBDAC1xy8sC3v5TfvsVob4fVIvsIJVI1ebPdM1j23DHWckndv9YI0d
	////////////////<YOUR FULL PRIVATE KEY>/////////////////////////
	qsOCOWaK62gsmchowEeOPgufVa4rLAevl8rXyqP85gf//4xiYge47gNBSkhEcXW4
	=IA1M
	-----END PGP PRIVATE KEY BLOCK-----'), 'yourPassphrase') AS decrypted_data FROM public.cc
2024-04-30 07:52:01.899 UTC [45] LOG:  duration: 799.849 ms
2024-04-30 07:52:01.900 UTC [45] LOG:  disconnection: session time: 0:00:00.804 user=postgres database=testdb host=172.21.0.1 port=60608
```

3. Logs when data is accessed through the `decrypt-data.py` script (without the `private.key`)

```log
2024-04-30 07:54:51.738 UTC [57] LOG:  connection received: host=172.21.0.1 port=53626
2024-04-30 07:54:51.740 UTC [57] LOG:  connection authenticated: identity="postgres" method=scram-sha-256 (/var/lib/postgresql/data/pg_hba.conf:128)
2024-04-30 07:54:51.740 UTC [57] LOG:  connection authorized: user=postgres database=testdb
2024-04-30 07:54:51.741 UTC [57] LOG:  statement: BEGIN
2024-04-30 07:54:51.741 UTC [57] LOG:  duration: 0.062 ms
2024-04-30 07:54:51.741 UTC [57] LOG:  statement: SELECT credit_card FROM public.cc
2024-04-30 07:54:51.741 UTC [57] LOG:  duration: 0.283 ms
2024-04-30 07:54:51.741 UTC [57] LOG:  disconnection: session time: 0:00:00.003 user=postgres database=testdb host=172.21.0.1 port=53626
```

## Contributors

<p align="left"> <b>Author : Kavindu Kalinga </b>
<a href="https://www.linkedin.com/in/kalingachandrasiri" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="kalingachandrasiri" height="15" width="20" /></a>
<a href="https://twitter.com/yuk_kalinga_c" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="kavindukalinga" height="15" width="20" /></a>
<a href="https://stackoverflow.com/users/16277941/kavindu-kalinga" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/stack-overflow.svg" alt="kavindu-kalinga" height="15" width="20" /></a>
<a href="https://www.facebook.com/kavindu.kalinga" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="kavindu.kalinga" height="15" width="20" /></a>
<a href="https://www.instagram.com/kavindu_kalinga" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="kavindu_kalinga" height="15" width="20" /></a>
<a href="https://discord.gg/CrazzyHawK#8536" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/discord.svg" alt="CrazzyHawK#8536" height="15" width="20" /></a>
</p>

<a href="https://github.com/kavindukalinga/PostgreSQL-Database-Encryption-using-Pgcrypto/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=kavindukalinga/PostgreSQL-Database-Encryption-using-Pgcrypto" />
</a>
