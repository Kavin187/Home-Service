import sqlite3
import streamlit as st
from twilio.rest import Client

# Twilio account details (Replace these with your actual Twilio account details)
account_sid = 'AC2b92cb2f110c614d2fdee90969408413'  # Replace with your Account SID
auth_token = '857bda83bba8e09651976c053c34fe0b'    # Replace with your Auth Token
 # Your Auth Token from twilio.com/console
twilio_phone_number = '+14088404551'  # Twilio phone number (e.g., +1234567890)

# Default recipient phone number (Replace with your phone number)
default_recipient_phone = '+918111084361'   

# Connect to SQLite database (or create it)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create a table with additional fields if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    phone_number TEXT,
    email TEXT,
    location TEXT,
    work_type TEXT,
    worker_name TEXT
)
''')
conn.commit()

# Input form
st.title("Registration Form")

name = st.text_input("Enter your Name")
age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)
phone_number = st.text_input("Enter your phone number")
email = st.text_input("Enter your email")
location = st.text_input("Enter your location")
work_type = st.text_input("Enter the type of work")
worker_name = st.text_input("Enter the worker's name")

if st.button("Submit"):
    # Insert data into the database
    if name and email and phone_number and location and work_type and worker_name:
        c.execute('''
            INSERT INTO users (name, age, phone_number, email, location, work_type, worker_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, phone_number, email, location, work_type, worker_name))
        conn.commit()
        st.success("Data stored successfully!")
    else:
        st.error("Please fill out all fields.")

# Button to send SMS using Twilio
if st.button("Book Worker"):
    if name and phone_number and location:
        try:
            # Create a Twilio client
            client = Client(account_sid, auth_token)

            # Compose the message (using the user's details)
            message_content = f"Name: {name}, Phone: {phone_number}, Location: {location}"

            # Send the message to the default recipient phone number
            message = client.messages.create(
                to=default_recipient_phone,  # Default recipient phone number
                from_=twilio_phone_number,  # Twilio phone number
                body=message_content
            )

            st.success(f"SMS sent successfully to {worker_name}")
        except Exception as e:
            st.error(f"Failed to send SMS: {e}")
    else:
        st.error("Please fill out the name, phone number, and location.")

# Close the connection
conn.close()
