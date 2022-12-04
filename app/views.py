# views.py

from flask import Flask, render_template, request, redirect
from qrcode import QRCode

def scan():
    if request.method == 'POST':
        # Read the QR code image file from the request
        image_file = request.files['qr_code']

        # Create a QRCode object
        qr = QRCode()

        # Scan the QR code image and extract the email address
        email = qr.scan(image_file)

        # Redirect to the user account page with the email address
        return redirect(f'/account?email={email}')

    else:
        # Return the QR code scanning page
        return render_template('scan.html')

def account():
    # Get the email address from the request query string
    email = request.args.get('email')

    # Return the user account page with the email address
    return render_template('account.html', email=email)
