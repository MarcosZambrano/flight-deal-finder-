#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests_cache
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
# Cache session for saving the API Requests' Responses.
# ----------------------- PROGRAM REQUIREMENTS -----------------------
# 1. Use the Sheety API to read the destination data from your Google Sheet. The sheet should already contain the airport IATA codes for each city (e.g. CDG for Paris, JFK for New York).

# 2. Use the SerpAPI Google Flights API to check for the cheapest flights for a defined departure date and a return date (COULD BE YOUR DESIRED FLIGHT ITINERARY FOR THE YEAR!!)

# 3. If the price is lower than the lowest price listed in the Google Sheet then send an email to your own GMAIL ACCOUNT (only works for Gmail) and update the rows with the lowest price found.

# 4. The email includes the departure airport IATA code, destination airport IATA code, flight price and flight dates.



session = requests_cache.CachedSession('flight_deal_finder_cache', expire_after=86400) # 24 hours needed for the session to expire, long session for the api requests.

data_manager = DataManager(session=session)

# Getting the current flights data stored in Google Sheets with the Sheety API.
current_flights_data = data_manager.get_flight_data()

current_flights_data = current_flights_data["flightDeals"]

flight_data = FlightData(current_flights_data=current_flights_data, session=session)

is_lower = flight_data.check_prices()

notification_manager = NotificationManager()

if is_lower != False:  # If the price of any of the searched flights is higher than its corresponding in the current flights data in Google Sheets.
    data_manager.update_flight_data(data=is_lower) # Calling the method for updating the data from the Google Sheets.
    notification_manager.send_emails(flights_sync=is_lower, current_data=current_flights_data)
    # CREATE EMAIL NOTIFICATION

if is_lower == False:
    print("NO FLIGHT DEALS FOUND LOWER THAN CURRENT!")
