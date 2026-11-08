#!/usr/bin/env python3
"""
Final HYROX Ticket Availability Scraper

This script successfully scrapes ticket availability from the HYROX race website.
Based on the user's requirements and the provided images, this implements the complete 5-step process.
"""

import time
import json
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hyrox_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TicketInfo:
    """Data class for ticket information"""
    category: str
    status: str
    price: str
    start_window: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None

class HyroxScraper:
    """Main scraper class for HYROX ticket availability"""
    
    def __init__(self, headless: bool = False):
        self.driver = None
        self.wait = None
        self.headless = headless
        self.base_url = "https://hyroxdach.com/find-your-race/"
        
    def setup_driver(self):
        """Initialize Chrome driver with options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Try to use system Chrome driver first
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Using system Chrome driver")
        except Exception as e:
            logger.warning(f"System Chrome driver failed: {e}")
            # Try with webdriver-manager as fallback
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("Using webdriver-manager Chrome driver")
            except Exception as e2:
                logger.error(f"All Chrome driver options failed: {e2}")
                raise
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 15)
        
        logger.info("Chrome driver initialized successfully")
    
    def navigate_to_race_page(self):
        """Step 1: Navigate to the main race finder page"""
        logger.info(f"Navigating to {self.base_url}")
        self.driver.get(self.base_url)
        time.sleep(5)
        
        # Wait for page to load
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logger.info("Race finder page loaded")
        
        # Handle cookie popup
        self.handle_cookie_popup()
    
    def handle_cookie_popup(self):
        """Handle the cookie consent popup"""
        try:
            logger.info("Looking for cookie popup...")
            time.sleep(2)
            
            # Use the exact XPath selector for the cookie accept button
            cookie_button = self.driver.find_elements(By.XPATH, "//*[@id='ac233-ext-0-255']")
            if cookie_button:
                logger.info("Found cookie accept button")
                if cookie_button[0].is_displayed() and cookie_button[0].is_enabled():
                    logger.info("Clicking cookie accept button")
                    cookie_button[0].click()
                    logger.info("Successfully clicked cookie accept button")
                    time.sleep(3)
                    return True
                else:
                    logger.info("Cookie button found but not clickable")
            else:
                logger.info("No cookie popup found or already handled")
            
            return False
            
        except Exception as e:
            logger.warning(f"Error handling cookie popup: {e}")
            return False
    
    def click_buy_tickets(self):
        """Step 2: Click on first available 'Buy Tickets' button"""
        try:
            logger.info("Looking for Buy Tickets button")
            
            # Use the exact XPath selector for the Buy Tickets button
            buy_tickets_button = self.driver.find_elements(By.XPATH, "//*[@id='us_grid_1']/div[1]/article[2]/div/a")
            if buy_tickets_button:
                logger.info("Found Buy Tickets button")
                if buy_tickets_button[0].is_displayed() and buy_tickets_button[0].is_enabled():
                    logger.info("Clicking Buy Tickets button")
                    buy_tickets_button[0].click()
                    logger.info("Successfully clicked Buy Tickets button")
                    time.sleep(3)
                    
                    current_url = self.driver.current_url
                    logger.info(f"Current URL after click: {current_url}")
                    return True
                else:
                    logger.error("Buy Tickets button found but not clickable")
            else:
                logger.error("Buy Tickets button not found")
            
            return False
                
        except Exception as e:
            logger.error(f"Error clicking 'Buy Tickets': {e}")
            return False
    
    def click_buy_tickets_here(self):
        """Step 3: Click 'Buy Tickets Here' on the event page"""
        try:
            logger.info("Looking for 'Buy Tickets Here' button")
            time.sleep(3)
            
            # Use the exact XPath selector for the Buy Tickets Here button
            buy_tickets_here_button = self.driver.find_elements(By.XPATH, "//*[@id='page-content']/section[1]/div[2]/div/div[2]/div/div/div[5]/div/div/div/div[5]/button")
            if buy_tickets_here_button:
                logger.info("Found Buy Tickets Here button")
                if buy_tickets_here_button[0].is_displayed() and buy_tickets_here_button[0].is_enabled():
                    logger.info("Clicking Buy Tickets Here button")
                    buy_tickets_here_button[0].click()
                    logger.info("Successfully clicked Buy Tickets Here button")
                    time.sleep(3)
                    return True
                else:
                    logger.error("Buy Tickets Here button found but not clickable")
            else:
                logger.error("Buy Tickets Here button not found")
            
            return False
                
        except Exception as e:
            logger.error(f"Error clicking 'Buy Tickets Here': {e}")
            return False
    
    def click_athlete_tickets(self):
        """Step 4: Click 'Athlete Tickets' in popup"""
        try:
            logger.info("Looking for 'Athlete Tickets' button")
            time.sleep(3)
            
            # Use the exact XPath selector for the Athlete Tickets button
            athlete_tickets_button = self.driver.find_elements(By.XPATH, "/html/body/div[8]/div/div/div/section/div/div/div/div/div/div/div/div/div/div/div[1]/a")
            if athlete_tickets_button:
                logger.info("Found Athlete Tickets button")
                if athlete_tickets_button[0].is_displayed() and athlete_tickets_button[0].is_enabled():
                    logger.info("Clicking Athlete Tickets button")
                    athlete_tickets_button[0].click()
                    logger.info("Successfully clicked Athlete Tickets button")
                    time.sleep(3)
                    return True
                else:
                    logger.error("Athlete Tickets button found but not clickable")
            else:
                logger.error("Athlete Tickets button not found")
            
            return False
            
        except Exception as e:
            logger.error(f"Error clicking 'Athlete Tickets': {e}")
            return False
    
    def scrape_ticket_availability(self) -> List[TicketInfo]:
        """Step 5: Scrape all available ticket information"""
        tickets = []
        
        try:
            logger.info("Scraping ticket information")
            time.sleep(3)
            
            # Wait for ticket page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Get page text
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            logger.info(f"Page text length: {len(page_text)}")
            
            # Look for ticket information patterns
            import re
            
            # Find all lines containing HYROX
            lines = page_text.split('\n')
            hyrox_lines = [line.strip() for line in lines if 'HYROX' in line and line.strip()]
            logger.info(f"Found {len(hyrox_lines)} lines containing 'HYROX'")
            
            # Process each HYROX line to extract ticket information
            for line in hyrox_lines:
                if any(day in line for day in ['Saturday', 'Sunday']):
                    # Extract basic info
                    category = line
                    status = "SOLD OUT" if "SOLD OUT" in line.upper() else "Available"
                    
                    # Look for price in nearby lines
                    price = ""
                    line_index = lines.index(line)
                    for i in range(max(0, line_index-3), min(len(lines), line_index+3)):
                        if "CHF" in lines[i]:
                            price_match = re.search(r'CHF\s*[\d,]+\.?\d*', lines[i])
                            if price_match:
                                price = price_match.group()
                                break
                    
                    # Look for start window
                    start_window = ""
                    for i in range(max(0, line_index-3), min(len(lines), line_index+3)):
                        time_match = re.search(r'\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}', lines[i])
                        if time_match:
                            start_window = time_match.group()
                            break
                    
                    # Extract date
                    date = ""
                    if "Saturday" in line:
                        date = "Saturday"
                    elif "Sunday" in line:
                        date = "Sunday"
                    
                    tickets.append(TicketInfo(
                        category=category,
                        status=status,
                        price=price,
                        start_window=start_window if start_window else None,
                        date=date if date else None
                    ))
            
            # If no tickets found with the above method, try alternative approach
            if not tickets:
                logger.info("No tickets found with standard method, trying alternative approach...")
                tickets = self._scrape_tickets_alternative()
            
            logger.info(f"Successfully scraped {len(tickets)} tickets")
            return tickets
            
        except Exception as e:
            logger.error(f"Error scraping ticket availability: {e}")
            return []
    
    def _scrape_tickets_alternative(self) -> List[TicketInfo]:
        """Alternative method to scrape tickets"""
        tickets = []
        try:
            # Look for any elements that might contain ticket information
            ticket_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'HYROX') or contains(text(), 'CHF') or contains(text(), 'Available') or contains(text(), 'SOLD OUT')]")
            
            for element in ticket_elements:
                text = element.text.strip()
                if text and len(text) > 10:  # Filter out very short text
                    # Try to extract ticket info from this element
                    if "HYROX" in text and any(day in text for day in ['Saturday', 'Sunday']):
                        category = text
                        status = "SOLD OUT" if "SOLD OUT" in text.upper() else "Available"
                        
                        # Look for price
                        import re
                        price_match = re.search(r'CHF\s*[\d,]+\.?\d*', text)
                        price = price_match.group() if price_match else ""
                        
                        tickets.append(TicketInfo(
                            category=category,
                            status=status,
                            price=price
                        ))
            
        except Exception as e:
            logger.warning(f"Alternative scraping method failed: {e}")
        
        return tickets
    
    def save_results(self, tickets: List[TicketInfo], filename: str = "hyrox_tickets.json"):
        """Save scraped results to JSON file"""
        try:
            data = [asdict(ticket) for ticket in tickets]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def print_results(self, tickets: List[TicketInfo]):
        """Print scraped results to console"""
        if not tickets:
            print("No tickets found!")
            return
        
        print(f"\n{'='*60}")
        print(f"HYROX TICKET AVAILABILITY - {len(tickets)} TICKETS FOUND")
        print(f"{'='*60}")
        
        for i, ticket in enumerate(tickets, 1):
            print(f"\n{i}. {ticket.category}")
            print(f"   Status: {ticket.status}")
            print(f"   Price: {ticket.price}")
            if ticket.start_window:
                print(f"   Start Window: {ticket.start_window}")
            if ticket.date:
                print(f"   Date: {ticket.date}")
            print("-" * 40)
    
    def run_scraper(self):
        """Main method to run the complete scraping process"""
        try:
            logger.info("Starting HYROX ticket scraper")
            
            # Setup
            self.setup_driver()
            
            # Step 1: Navigate to race page
            self.navigate_to_race_page()
            
            # Step 2: Click Buy Tickets
            if not self.click_buy_tickets():
                logger.error("Failed to click 'Buy Tickets'")
                return []
            
            # Step 3: Click Buy Tickets Here
            if not self.click_buy_tickets_here():
                logger.error("Failed to click 'Buy Tickets Here'")
                return []
            
            # Step 4: Click Athlete Tickets
            if not self.click_athlete_tickets():
                logger.error("Failed to click 'Athlete Tickets'")
                return []
            
            # Step 5: Scrape tickets
            tickets = self.scrape_ticket_availability()
            
            # Display and save results
            self.print_results(tickets)
            self.save_results(tickets)
            
            return tickets
            
        except Exception as e:
            logger.error(f"Scraper failed: {e}")
            return []
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("Driver closed")

def main():
    """Main function to run the scraper"""
    scraper = HyroxScraper(headless=False)  # Set to True for headless mode
    tickets = scraper.run_scraper()
    
    if tickets:
        print(f"\nScraping completed successfully! Found {len(tickets)} tickets.")
    else:
        print("\nScraping failed or no tickets found.")

if __name__ == "__main__":
    main()