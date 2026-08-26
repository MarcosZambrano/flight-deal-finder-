import os
import requests 
import requests_cache
from dotenv import load_dotenv

load_dotenv()

SHEETY_API_KEY = os.environ["SHEETY_API_KEY"]
SERP_API_KEY = os.environ["SERP_API_KEY"]
SHEETY_ID = os.environ["SHEETY_ID"]

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self, session):
        self.flight_data = {}
        self.session = session

    def get_flight_data(self): # SHEETY API CALL
        url = f"https://api.sheety.co/{SHEETY_ID}/flightDeals/flightDeals"

        header = {
            "Authorization": f"Bearer {SHEETY_API_KEY}"
        }

        response = self.session.get(url=url, headers=header)
        self.flight_data = response.json()

        print(f"Current flight data: {self.flight_data}")

        return self.flight_data

    def update_flight_data(self, data):
        print()
        print("Flights to synchronize: ")
        # print(data)
        index = 0
        
        for flight in data:
            """ 
             Validations to make: 
             1. Departure Id
             2. Destination Id
             3. Lowest Price
             4. Departure Date
             5. Return Date
            """

            print("DATA FROM FLIGHTS TO SYNCHRONIZE:")
            print()
            
            print(f"Departure airport: {flight["flights"][0]["departure_airport"]["id"]}")
            print(f"Arrival airport: {flight["flights"][-1]["arrival_airport"]["id"]}")
            print(f"Ticket price: {flight["price"]}")
            print(f"Departure date: {flight["flights"][0]["departure_airport"]["time"][:10]}")

            print("--------------------------------------------------------")
            print("")
            print("CURRENT GOOGLE SHEETS DATA: ")
            print("")
            print(f"Departure ID: {self.flight_data["flightDeals"][index]["departureId"]}")
            print(f"Destination ID: {self.flight_data["flightDeals"][index]["destinationId"]}")
            print(f"Lowest Price: {self.flight_data["flightDeals"][index]["lowestPrice"]}")
            print(f"Departure Date: {self.flight_data["flightDeals"][index]["departureDate"]}")
            print(f"Return Date: {self.flight_data["flightDeals"][index]["returnDate"]}")

            if (flight["flights"][0]["departure_airport"]["id"] == self.flight_data["flightDeals"][index]["departureId"] and 
            flight["flights"][-1]["arrival_airport"]["id"] == self.flight_data["flightDeals"][index]["destinationId"] and
            flight["flights"][0]["departure_airport"]["time"][:10] == self.flight_data["flightDeals"][index]["departureDate"]) :

                url = f"https://api.sheety.co/{SHEETY_ID}/flightDeals/flightDeals/{self.flight_data['flightDeals'][index]['id']}"

                header = {
                    "Authorization": f"Bearer {SHEETY_API_KEY}"
                }

                body = {
                    "flightdeal": {
                        "departureCity": self.flight_data["flightDeals"][index]["departureCity"],
                        "departureId": self.flight_data["flightDeals"][index]["departureId"],
                        "destinationId": self.flight_data["flightDeals"][index]["destinationId"],
                        "destinationCity": self.flight_data["flightDeals"][index]["destinationCity"],
                        "lowestPrice": flight["price"], # This is the updated price gotten from Search SERP API.
                        "departureDate": self.flight_data["flightDeals"][index]["departureDate"],
                        "returnDate": self.flight_data["flightDeals"][index]["returnDate"]
                    }
                }

                response = requests.put(url=url, headers=header, json=body)
                print(response.text)
                response.raise_for_status()

            index = index + 1

            
            

              
