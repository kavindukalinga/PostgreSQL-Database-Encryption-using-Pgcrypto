import psycopg2
import subprocess

# Database configuration
DB_HOST = 'localhost'
DB_PORT = '5436'
DB_NAME = 'testdb'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# Function to decrypt data using GPG and private key file
def decrypt_data(data, private_key_path):
    process = subprocess.Popen(['gpg', '--decrypt', '--batch', '--quiet', '--pinentry-mode', 'loopback', '--passphrase-file', 'kk.txt'], 
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    decrypted_data, _ = process.communicate(input=data)
    return decrypted_data

# Define a function to connect to the database and retrieve encrypted data
def get_encrypted_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT credit_card FROM public.cc")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Decrypt encrypted data
# Decrypt encrypted data
def decrypt_rows(rows, private_key_path):
    decrypted_rows = []
    for row in rows:
        bytea_data = row[0]  # Get bytea data from the row
        # Convert bytea data to byte string
        encrypted_data = bytes(bytea_data)
        # Decrypt the byte string
        try:
            decrypted_data = decrypt_data(encrypted_data, private_key_path)
            decrypted_rows.append(decrypted_data.decode('utf-8'))
        except Exception as e:
            print(f"Error decrypting data: {e}")
            decrypted_rows.append("Decryption Error")
    return decrypted_rows


# Open the private key file in binary mode
def main():
    private_key_path = "./keys/private.key"  # Update with the path to your private key file
    encrypted_data_rows = get_encrypted_data()
    decrypted_data_rows = decrypt_rows(encrypted_data_rows, private_key_path)
    for decrypted_data in decrypted_data_rows:
        print("Decrypted Data:", decrypted_data)

if __name__ == "__main__":
    main()
