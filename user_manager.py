import os
import requests 
import requests_cache
from dotenv import load_dotenv

load_dotenv()

SHEETY_API_KEY = os.environ["SHEETY_API_KEY"]
SERP_API_KEY = os.environ["SERP_API_KEY"]

class UserManager:
    # This class is responsible for the management users: getting new user inputs, creating new users, and getting user data.
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.email = ""

    def new_user_input(self):
        # Method that gets the data from the users through the console.
        print("----- BECOME A MEMBER OF FLIGHT CLUB -----")
        self.first_name = input("First name: ")
        self.last_name = input("Last name: ")
        self.email = input("Email: ")
        # print(self.first_name)
        # print(self.last_name)
        # print(self.email)

    def create_user(self):
        # Method that adds the row of the new user into the users sheet through the Sheety API.
        print("Creating user in Google Sheets...")

        url = "https://api.sheety.co/16e5ddb843d4b041658adc1425494e72/flightDeals/users"

        header = {
            "Authorization": f"Bearer {SHEETY_API_KEY}"
        }

        body = {
            "user": {
                "firstName": self.first_name,
                "lastName": self.last_name,
                "email": self.email
                }
            }

        response = requests.post(url=url, headers=header, json=body)
        print(response.text)
        response.raise_for_status()

    def get_user_data(self):
        # Method that gets the user data and returns it as a dictionary.
        url = "https://api.sheety.co/16e5ddb843d4b041658adc1425494e72/flightDeals/users"

        header = {
            "Authorization": f"Bearer {SHEETY_API_KEY}"
        }

        response = requests.get(url=url, headers=header)
        print(response.text)
        response.raise_for_status()
        current_users_data = response.json()
        print(current_users_data)
        return current_users_data


