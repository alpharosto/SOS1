from flask import Flask, request, jsonify
from twilio.rest import Client
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# API endpoint for sending messages
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json

    # Extract message details from request
    to_numbers = data.get('to_numbers', [])
    message_body = data.get('message_body', '')

    # Send messages to designated contacts
    for to_number in to_numbers:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )

        print("Message sent to", to_number, "Message SID:", message.sid)

    return jsonify({"message": "Messages sent successfully"}), 200

# Root endpoint to display a hello message
@app.route('/')
def hello():
    return 'Hello! Welcome to the Twilio Messaging Service.', 200

if __name__ == '__main__':
    app.run(debug=True)
