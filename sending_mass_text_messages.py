
import csv
import logging
import os
from time import sleep
from twilio.rest import Client
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

# Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

# Create a Twilio client
client = Client(account_sid, auth_token)

# Message content
message_body = 'Hello from Twilio!'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to send SMS with retry mechanism
def send_sms(to_phone_number, from_phone_number, message, retries=3):
    for attempt in range(retries):
        try:
            message = client.messages.create(
                to=to_phone_number,
                from_=from_phone_number,
                body=message
            )
            logging.info(f"Message sent to {to_phone_number}: {message.sid}")
            return True
        except Exception as e:
            logging.error(f"Failed to send message to {to_phone_number}: {e}")
            if attempt < retries - 1:
                sleep(1)  # Wait before retrying
    return False

# Function to read phone numbers from CSV file and send messages
def send_mass_sms(file_path, rate_limit_per_sec=1):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            phone_number = row['phone_number']
            send_sms(phone_number, twilio_phone_number, message_body)
            sleep(1 / rate_limit_per_sec)  # Rate limiting to 1 message per second

# Path to the CSV file
# csv_file_path = 'phone_numbers.csv'
csv_file_path = 'C:\\Users\\Anuj\\AppData\\Local\\Programs\\Python\\Python312\\Botteleg.py\\sending_mass_messages\\phone_numbers.csv'


# Sending up to 3600 messages per hour
send_mass_sms(csv_file_path)


# from twilio.rest import Client

# # Your Account SID from twilio.com/console
# account_sid = 'AC4d7bec2ec41941b9a3c4d9b4a5b49cde'
# # Your Auth Token from twilio.com/console
# auth_token = '713efbaf8c16f71ada3f82dfe84d7b16'

# client = Client(account_sid, auth_token)

# message = client.messages.create(
#     to='+918171916543',  # Recipient's phone number
#     from_='+16056092499',  # Your Twilio phone number
#     body='Hello from Twilio!'
# )

# print(message.sid)
