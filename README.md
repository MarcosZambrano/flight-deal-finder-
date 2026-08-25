# ✈️ Flight Deal Finder

An automated flight price tracker that reads your desired destinations from a Google Sheet via SHEETY API, checks current flight prices via SerpAPI's Google Flights engine, and emails you when it finds a deal cheaper than your target price — updating the sheet with the new lowest price.

## How it works

1. **Read destinations** — Pulls departure/destination airport IATA codes and target prices from a Google Sheet via the [Sheety](https://sheety.co/) API.
2. **Search flights** — Queries [SerpAPI's Google Flights engine](https://serpapi.com/google-flights-api) for each route, sorted by price.
3. **Compare prices** — If the cheapest result is lower than the price stored in the sheet, the flight is flagged as a deal.
4. **Notify & update** — Sends an email (via Gmail SMTP) with the deal details and updates the corresponding row in the Google Sheet with the new lowest price.

If no flight beats the current lowest price, the script simply logs that no deals were found.

## Project structure

| File | Responsibility |
|---|---|
| [main.py](main.py) | Orchestrates the workflow: fetch sheet data → check prices → sync sheet → send emails |
| [data_manager.py](data_manager.py) | Talks to the Google Sheet through the Sheety API (read and update flight rows) |
| [flight_search.py](flight_search.py) | Talks to the SerpAPI Google Flights endpoint to search for flights |
| [flight_data.py](flight_data.py) | Compares search results against the sheet's stored prices and builds the list of deals to sync |
| [notification_manager.py](notification_manager.py) | Sends deal-alert emails over Gmail's SMTP server |

An `requests_cache` session (24h expiry) is shared across API calls to reduce redundant requests.

## Google Sheet format

Your Sheety-backed Google Sheet (`flightDeals` tab) should have these columns:

| departureCity | departureId | destinationCity | destinationId | lowestPrice | departureDate | returnDate |
|---|---|---|---|---|---|---|
| London | LON | Paris | CDG | 60 | 2026-09-01 | 2026-09-10 |

- `departureId` / `destinationId` are IATA airport codes.
- `lowestPrice` is the current price threshold — a search result must be lower than this to trigger an alert.
- Dates use `YYYY-MM-DD` format.

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

> Update the Sheety endpoint URL in [data_manager.py](data_manager.py) to point at your own Google Sheet project.

### 3. Run

```bash
python main.py
```

## Notes

- Prices are searched in EUR (`currency: "EUR"` in the SerpAPI request body).
- The notification email's recipient is currently hardcoded in [notification_manager.py](notification_manager.py) — update it to your own address if reusing this project.
- `flight_deal_finder_cache.sqlite` (the request cache) and `.env` are git-ignored.
