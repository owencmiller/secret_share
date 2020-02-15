from flask import Flask, request
from flask import render_template
import hashlib
from cryptography.fernet import Fernet

app = Flask(__name__)

data = {}


@app.route('/')
def index():
    return render_template('index.html')


def generateLink(key):
    return '/getsecret/' + key.decode()


@app.route('/sharesecret', methods=['POST'])
def sharing():
    key = Fernet.generate_key()  # this is your "password"
    cipher_suite = Fernet(key)
    encoded_text = cipher_suite.encrypt(request.form['secret'].encode())
    data[hashlib.sha256(key).digest()] = encoded_text
    print('saving secret')
    return render_template('index.html', link=generateLink(key))


@app.route('/getsecret/<key>', methods=['GET'])
def receiving(key):
    hash = hashlib.sha256(key.encode()).digest()
    if hash in data.keys():
        cipher_suite = Fernet(key)
        decoded_text = cipher_suite.decrypt(data.pop(hash))
        print('returning secret')
        return render_template('index.html', secret=decoded_text.decode())
    else:
        print('secret not found')
        return render_template('index.html', error='No secret found')


if __name__ == '__main__':
    app.run("0.0.0.0", port="8080")
