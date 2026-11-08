# HYROX Ticket Scraper

This script opens the HYROX DACH race page in Chrome, goes to the athlete tickets of one race, and gets the ticket categories, prices, and availability.

## What it does

- Starts Google Chrome with Selenium.
- Opens `https://hyroxdach.com/find-your-race/` and accepts the cookie popup.
- Clicks through the ticket pages of one race.
- Reads the ticket category, the status (Available or SOLD OUT), the price in CHF, the start window, and the day.
- Shows the tickets in the terminal.
- Writes the tickets to `hyrox_tickets.json` and the run log to `hyrox_scraper.log`.

## Requirements

- Python 3.9 or newer
- Google Chrome
- An internet connection

## Install

1. Clone the repository:

   ```bash
   git clone https://github.com/Ikarus0013/hyrox-ticket-scraper.git
   cd hyrox-ticket-scraper
   ```

2. Make a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

Selenium gets a ChromeDriver that matches your Chrome version. You do not need to install ChromeDriver yourself.

## Configure

The script needs no API keys and no environment variables.

The default mode shows the Chrome window. To use headless mode, change this line in the `main()` function of `hyrox_scraper_final.py`:

```python
scraper = HyroxScraper(headless=True)
```

## Use

1. Start the script:

   ```bash
   python hyrox_scraper_final.py
   ```

2. Do not use the Chrome window while the script runs.
3. Wait until the script stops. It closes Chrome when it is done.

The terminal shows each ticket. This example shows the format. The values are not real:

```text
1. HYROX MEN | Saturday
   Status: Available
   Price: CHF 129.00
   Start Window: 08:00 - 13:50
   Date: Saturday
```

The script also writes these files in the current folder:

| File | Content |
|---|---|
| `hyrox_tickets.json` | List of tickets with the keys `category`, `status`, `price`, `start_window`, `description`, and `date` |
| `hyrox_scraper.log` | Log of each step |

If a step fails, the log shows the step. The JSON file then contains an empty list.

## How it works

The script does 5 steps:

1. Open the race page and accept the cookie popup.
2. Click **Buy Tickets** on one race.
3. Click **Buy Tickets Here** on the event page.
4. Click **Athlete Tickets** in the popup.
5. Read the page text. Find the lines with "HYROX" and "Saturday" or "Sunday". Find the price and the start window in the lines near them.

If step 5 finds no tickets, the script tries a second method. It reads all page elements that contain "HYROX", "CHF", "Available", or "SOLD OUT".

## Files

| File | Description |
|---|---|
| `hyrox_scraper_final.py` | The scraper |
| `requirements.txt` | Python dependencies |

## Limits

- The script finds the buttons with fixed XPath selectors and a fixed cookie button id. If the website changes its layout, the script stops working.
- Step 2 always uses the same position in the race list. It does not let you select a race.
- The ticket text patterns are for prices in CHF and for Saturday and Sunday events.
- In the last test run, the script did all click steps but found 0 tickets. Check the selectors before you use the results.
- The script hides some automation signals of Chrome. Respect the terms of use of the website and `robots.txt`. Use the script only for personal, low-volume checks.

## License

MIT. See [LICENSE](LICENSE).
