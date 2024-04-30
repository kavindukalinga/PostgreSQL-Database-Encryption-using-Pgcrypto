from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database configuration
DB_HOST = 'localhost'
DB_PORT = '5436'
DB_NAME = 'testdb'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# Open the file in binary mode
with open('./keys/private.key', 'rb') as f:
    file_content_bytes = f.read()
# Decode the bytes to a string using the appropriate character encoding
PRIVATE_KEY = file_content_bytes.decode('utf-8')

# Define a function to connect to the database and retrieve data
def get_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT customer_id, pgp_pub_decrypt(credit_card, dearmor(%s), 'kalinga') AS decrypted_data FROM public.cc", (PRIVATE_KEY,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Define a route to store data
@app.route('/store_data/<int:customer_id>/<string:credit_card>')
def store_data(customer_id, credit_card):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        query=f"INSERT INTO cc(customer_id,credit_card) VALUES ({customer_id},pgp_pub_encrypt('{credit_card}',dearmor(pg_read_file('keys/public.key'))));"
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return 'Data stored successfully'
    except Exception as e:
        return str(e)

# Define a route to fetch data
@app.route('/get_data')
def fetch_data():
    try:
        data = get_data()
        response = [{'customer_id': row[0], 'decrypted_data': row[1]} for row in data]
        return jsonify(response)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
