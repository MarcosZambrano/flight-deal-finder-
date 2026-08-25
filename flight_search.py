import os
import requests 
import requests_cache
from dotenv import load_dotenv

load_dotenv()

SHEETY_API_KEY = os.environ["SHEETY_API_KEY"]
SERP_API_KEY = os.environ["SERP_API_KEY"]

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self, session):
        self.flight_search = {}
        self.session = session

    def get_flight_search(self, departure_id, destination_id, departure_date, return_date, max_price):
        """ In this method we will get the search results for the flights with the corresponding departure and arrival airports to our desired destinations (that came from Google Sheets) """

        url = "https://serpapi.com/search?engine=google_flights"

        body = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "currency": "EUR",
            "arrival_id": destination_id,
            "api_key": SERP_API_KEY,
            "outbound_date": departure_date,
            "return_date": return_date,
            "max_price": max_price,
            "sort_by": 2
        } 

        print("Body for the SERP API HTTP REQUEST:")
        print()
        print(body)
        print()

        response = self.session.get(url=url, params=body)
        self.flight_search = response.json()
        print("FLIGHT SEARCH RESPONSE FROM SERP API")
        print()
        print(self.flight_search)
        print()

        return self.flight_search
        # print(departure_id)
        # print(arrival_id)



