from flask import Flask, render_template, request, redirect
from app.views import scan, account
import os

app = Flask(__name__)

# Set the FLASK_APP environment variable
os.environ.setdefault('FLASK_APP', 'app')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scan')
def scan():
    # Code to handle a user scanning a QR code here
    return render_template('scan.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate the user's username and password
        user = authenticate(username, password)
        if user:
            # If the authentication is successful, redirect to the list of camps
            return redirect('/camps')
        else:
            # If the authentication is unsuccessful, display an error message
            error_msg = "Invalid username or password"
            return render_template('login.html', error_msg=error_msg)
    else:
        return render_template('login.html')



#@app.route('/account')
#def account():
# Code for the account view function