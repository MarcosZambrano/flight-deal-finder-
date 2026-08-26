import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import time

SENDER_EMAIL = os.getenv("EMAIL")
SENDER_PASSWORD = os.getenv("APP_PASSWORD")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.subject = ""
        self.content = ""
        
    def send_emails(self, flights_sync, current_data, users_data):
        # Strict Guard Clause
        print(f"CURRENT DATA FROM EMAIL NOTIFICATION MANAGER")
        print(current_data)
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            raise ValueError("Missing essential credentials! Check that your local .env file is populated.")

        try:
            # Establishing a connection to the SMTP Server.
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.ehlo()          
                connection.starttls()      
                connection.ehlo()          
                connection.login(user=SENDER_EMAIL, password=SENDER_PASSWORD)

                index = 0

                for flight in flights_sync:
                    for user in users_data["users"]:
                        
                        content = f"Low price alert! This is cheaper than your target price.\n\n{current_data[index]["departureCity"]} ({flight["flights"][0]["departure_airport"]["id"]}) → {current_data[index]["destinationCity"]} ({flight["flights"][-1]["arrival_airport"]["id"]})\n\nDeparture: {flight["flights"][0]["departure_airport"]["time"][:10]} at {flight["flights"][0]["departure_airport"]["time"][11:16]}\nReturn: {current_data[index]["returnDate"]}\n\nNew price: €{flight["price"]}\n\nEmail sent from your Flight Deal Finder"

                        # Content structural generation
                        msg = EmailMessage()
                        msg["Subject"] = f"✈️ {user["firstName"]}! You have a Flight Deal Alert: {current_data[index]["departureCity"]} → {current_data[index]["destinationCity"]} for €{flight["price"]}!"
                        msg["From"] = SENDER_EMAIL
                        msg["To"] = f"{user["email"]}"
                        msg.set_content(content)

                        # Single message transmission payload dispatch
                        try:
                            connection.send_message(msg)
                            print(f"[SUCCESS] Dispatched delivery of new flight deal notification to {user["email"]}")
                        except smtplib.SMTPException as recipient_err:
                            print(f"[DELIVERY FAILURE] Error sending email: {type(recipient_err).__name__} - {recipient_err}")
                            continue

                    index = index + 1
                    time.sleep(5)

        except smtplib.SMTPAuthenticationError:
            print("[AUTHENTICATION CRITICAL] SMTP Gateway denied credentials. Verify your App Password settings.")
        except (smtplib.SMTPConnectError, OSError) as network_err:
            print(f"[NETWORK CRITICAL] Connection failed. Sockets could not resolve remote host: {network_err}")
        