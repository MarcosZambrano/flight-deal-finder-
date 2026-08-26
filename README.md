# ✈️ Flight Deal Finder

An automated flight price tracker that registers users, reads your desired destinations from a Google Sheet via the Sheety API, checks current flight prices via SerpAPI's Google Flights engine, and emails every subscribed user a personalized alert when it finds a deal cheaper than your target price — updating the sheet with the new lowest price.

## How it works

1. **Register a user** — Prompts for a first name, last name, and email in the console, then adds the new user as a row in the Google Sheet's `users` tab via the Sheety API.
2. **Read destinations** — Pulls departure/destination airport IATA codes and target prices from the `flightDeals` tab via the [Sheety](https://sheety.co/) API.
3. **Search flights** — Queries [SerpAPI's Google Flights engine](https://serpapi.com/google-flights-api) for each route, sorted by price.
4. **Compare prices** — If the cheapest result is lower than the price stored in the sheet, the flight is flagged as a deal.
5. **Notify & update** — Updates the corresponding row in the Google Sheet with the new lowest price, then sends a personalized email (via Gmail SMTP) to every user in the `users` sheet, with the departure/destination airport codes, price, and flight dates.

If no flight beats the current lowest price, the script simply logs that no deals were found.

## Project structure

| File | Responsibility |
|---|---|
| [main.py](main.py) | Orchestrates the workflow: register user → fetch sheet data → check prices → sync sheet → send emails |
| [user_manager.py](user_manager.py) | Prompts for new user details on the console, adds them to the `users` sheet, and fetches all registered users via the Sheety API |
| [data_manager.py](data_manager.py) | Talks to the Google Sheet through the Sheety API (read and update flight rows) |
| [flight_search.py](flight_search.py) | Talks to the SerpAPI Google Flights endpoint to search for flights |
| [flight_data.py](flight_data.py) | Compares search results against the sheet's stored prices and builds the list of deals to sync |
| [notification_manager.py](notification_manager.py) | Sends a personalized deal-alert email to each subscribed user over Gmail's SMTP server |

An `requests_cache` session (24h expiry) is shared across the flight-search API calls to reduce redundant requests.

## Google Sheet format

Your Sheety-backed Google Sheet needs two tabs:

**`flightDeals` tab**

| departureCity | departureId | destinationCity | destinationId | lowestPrice | departureDate | returnDate |
|---|---|---|---|---|---|---|
| London | LON | Paris | CDG | 60 | 2026-09-01 | 2026-09-10 |

- `departureId` / `destinationId` are IATA airport codes.
- `lowestPrice` is the current price threshold — a search result must be lower than this to trigger an alert.
- Dates use `YYYY-MM-DD` format.

**`users` tab**

| firstName | lastName | email |
|---|---|---|
| Jane | Doe | jane@example.com |

New rows are appended here automatically each time the script runs and a new user registers.

## Setup

### 1. Install dependencies

```bash
pip install requests requests_cache python-dotenv
```

### 2. Create a `.env` file

In the project folder, create a `.env` file with:

```
SHEETY_API_KEY=your_sheety_api_key
SERP_API_KEY=your_serpapi_key
EMAIL=your_gmail_address@gmail.com
APP_PASSWORD=your_gmail_app_password
```

- **SHEETY_API_KEY**: Bearer token for your Sheety project (from [sheety.co](https://sheety.co/)).
- **SERP_API_KEY**: API key from [serpapi.com](https://serpapi.com/).
- **EMAIL / APP_PASSWORD**: Your Gmail address and a Gmail [App Password](https://myaccount.google.com/apppasswords) (regular passwords won't work with SMTP if 2FA is enabled).

> Update the Sheety endpoint URLs in [data_manager.py](data_manager.py) and [user_manager.py](user_manager.py) to point at your own Google Sheet project.

### 3. Run

```bash
python main.py
```

You'll be prompted to enter a new user's first name, last name, and email before the flight search runs.

## Notes

- Prices are searched in EUR (`currency: "EUR"` in the SerpAPI request body).
- Emails are sent to every user currently in the `users` sheet, with a short delay between sends to avoid rate limits.
- `flight_deal_finder_cache.sqlite` (the request cache) and `.env` are git-ignored.