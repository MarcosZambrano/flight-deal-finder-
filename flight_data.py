from flight_search import FlightSearch
from pprint import pprint

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, current_flights_data, session):
        self.current_flights_data = current_flights_data
        self.session = session

    def check_prices(self):
        # This method is supposed to compare the flight searches to the current flight data that comes from Google Sheets.
        flights_to_sync = [] 
        flight_search = FlightSearch(session=self.session)
        for flight in self.current_flights_data:

            # print(flight)
            print(f"Evaluating the options for a flight from {flight["departureId"]} to {flight["destinationId"]}")
            
            flight_search_data = flight_search.get_flight_search(
                departure_id=flight["departureId"], 
                destination_id=flight["destinationId"], 
                departure_date=flight["departureDate"], 
                return_date=flight["returnDate"],
                max_price=flight["lowestPrice"]
            )

            # for flight_search in flight_search_data["other_flights"]: IF WE WANT TO COMPARE EVERY VALUE FROM THE SEARCH OF FLIGHTS,
            # WHICH IS NOT NECESSARY WHEN YOU SORT BY PRICE INSIDE OF THE API REQUEST.
            #     # pprint(flight_search)
            #     print()
            #     print()
            #     print(flight_search["price"])
            # Checking if the searched price is lower than the current lowest price.
            print()
            # print(flight_search_data)
            print()
            print()
            try:
                search_flight_price = flight_search_data["other_flights"][0]["price"] # Lowest price on the search. Because of value SORT BY in the API Request.
            except: # FOR THE CASE GOOGLE FLIGHTS API DID NOT RETURN ANY RESULTS.
                continue
            print(f"Price of the flight: {search_flight_price}")
            if search_flight_price < flight["lowestPrice"]:
                print(f"Searched price ({search_flight_price}) is lower than Excel's current price ({flight["lowestPrice"]}). Appending flight to flights_to_sync[]...")

                # Return the dictionary with all of the data from the flight_search.
                flights_to_sync.append(flight_search_data["other_flights"][0]) 

            else:
                print(f"Searched price ({search_flight_price}) is NOT lower than Excel's current price ({flight["lowestPrice"]}).")

                continue

        # Checking that the length of the list has more than 1 so I can return the list.
        if len(flights_to_sync) >= 1: 
            return flights_to_sync

        # If list is empty then return False.
        else:
            return False 
                

            
            # pprint(flight_search_data["other_flights"], indent=4)

            


