from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import time, random

def get_prompt_input_variables_from_state(state, prompt):
    return {k:v for k,v in state.__dict__.items() if k in prompt.input_variables}


def search_flights(origin: str, destination: str, date: str) -> List[Dict]:
    """
    Search for flights on major travel websites using web scraping.
    """
    flights = []
    websites = [
        {
            "name": "Skyscanner",
            "url": f"https://www.skyscanner.com/transport/flights/{origin}/{destination}/{date}/"
        },
        {
            "name": "Kayak",
            "url": f"https://www.kayak.com/flights/{origin}-{destination}/{date}"
        },
        {
            "name": "Expedia",
            "url": f"https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{origin},to:{destination},departure:{date}"
        }
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for website in websites:
        try:
            response = requests.get(website["url"], headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            if website["name"] == "Skyscanner":
                flight_elements = soup.find_all('div', class_='BpkTicket_bpk-ticket__YWNmY')
                for element in flight_elements[:3]:  # Limit to first 3 results
                    airline = element.find('span', class_='BpkText_bpk-text__ZmFkZ').text.strip()
                    price = element.find('span', class_='BpkText_bpk-text__ZWY3M').text.strip()
                    duration = element.find('span', class_='BpkText_bpk-text__MzY2N').text.strip()
                    flights.append({"website": website["name"], "airline": airline, "price": price, "duration": duration})

            elif website["name"] == "Kayak":
                flight_elements = soup.find_all('div', class_='Base-Results-HorizonResult')
                for element in flight_elements[:3]:
                    airline = element.find('div', class_='bottom').text.strip()
                    price = element.find('span', class_='price-text').text.strip()
                    duration = element.find('div', class_='duration').text.strip()
                    flights.append({"website": website["name"], "airline": airline, "price": price, "duration": duration})

            elif website["name"] == "Expedia":
                flight_elements = soup.find_all('li', class_='flight-module')
                for element in flight_elements[:3]:
                    airline = element.find('span', class_='airline-name').text.strip()
                    price = element.find('span', class_='price-column').text.strip()
                    duration = element.find('span', class_='duration-emphasis').text.strip()
                    flights.append({"website": website["name"], "airline": airline, "price": price, "duration": duration})

        except requests.RequestException as e:
            print(f"Error scraping {website['name']}: {str(e)}")
        except BaseException as e:
            print(f"Unexpected error scraping {website['name']}: {str(e)}")
        # Add a delay between requests to avoid overwhelming the servers
        time.sleep(random.uniform(1, 3))

    return flights
