from flask import Flask, render_template, request, redirect
import os
import openpyxl
from io import BytesIO
from PIL import Image
from time import sleep
import cv2
from pyzxing import BarCodeReader

app = Flask(__name__)

# Set the FLASK_APP environment variable
os.environ.setdefault('FLASK_APP', 'app')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/scan', methods=['GET', 'POST'])
def scan():
    # Initialize the QR code reader
    reader = cv2.QRCodeDetector()

    # Capture frames from the user's camera
    cam = cv2.VideoCapture(0)

    # Flag to track whether a QR code has been decoded
    qr_decoded = False
    while not qr_decoded:
        # Read a frame from the camera
        _, frame = cam.read()

        # Decode any QR codes in the frame
        data, bbox, _ = reader.detectAndDecode(frame)
        if data:
            # Set the flag to true
            qr_decoded = True

        # Display the frame to the user
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the camera and destroy the window displaying the video feed
    cam.release()
    cv2.destroyAllWindows()

    if not data:
        return render_template('scan.html', error='Failed to decode QR code')

    # At this point, the variable 'data' should contain the data from the QR code.

    # Extract the first and last names from the QR code data
    # Assume the data is encoded as "first_name last_name"
    try:
        first_name, last_name = qr_data.split(' ')
    except:
        return render_template('scan.html', error='QR code data is not in the expected format')


    # Open the Excel file and search for the customer's name on the roster
    excel_file = openpyxl.load_workbook('roster.xlsx')
    sheet = excel_file.get_sheet_by_name('Sheet1')  # Assume the roster is on the first sheet
    found = False
    for row in sheet.rows:
        if row[0].value == first_name and row[1].value == last_name:
            # Assume the first and last names are in the first and second columns
            found = True
            break

    if found:
        # Customer's name was found on the roster
        return render_template('scan.html', found=True)
    else:
        # Customer's name was not found on the roster
        return render_template('scan.html', found=False)





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
