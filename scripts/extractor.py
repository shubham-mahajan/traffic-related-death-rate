from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import csv
import json
import datetime

# Output Directory Location
output_dir = '../data/'


"""
Method to create CSV from the JSON Data
@params
    - json_data -> Contains Json Data
    - filename -> Name of the File for storage of CSV.
"""


def create_csv(json_data, filename):
    with open(filename, "w", newline="") as f:
        title = "Country,Continent,Road Fatalities Inhabitants per 10 Million,Road Fatalities Vehicles per 10 Million,Road Fatalities Vehicles per 1 Billion".split(
            ",")
        cw = csv.DictWriter(f, title, delimiter=',')
        cw.writeheader()
        cw.writerows(json_data)


"""
Method to Fetch the Page from the URL
@params 
    - url -> URL of Location need to be Fetched
@return
    - BeautifulSoup Object
"""


def get_data(url):
    response = urlopen(url)
    return BeautifulSoup(response)


"""
Method to convert the Montly Price Data to CSV
"""


def traffic_death_rate():
    soup = get_data(
        'https://en.wikipedia.org/wiki/List_of_countries_by_traffic-related_death_rate')

    data = []
    final_data = []
    for items in soup.find('table', class_='wikitable').find_all('tr')[1::1]:
        data = items.find_all(['th', 'td'])
        try:
            if data[1].text:
                country = data[0].text.strip()
                continent = data[1].text.strip()
                r_f_per_inhabitat_ten_million = data[1].find_next_sibling(
                ).text.strip()
                r_f_per_vehicle_ten_million = data[2].find_next_sibling(
                ).text.strip()
                r_f_per_vehicle_one_billion = data[3].find_next_sibling(
                ).text.strip()
                final_data.append({
                    "Country": country,
                    "Continent": continent,
                    "Road Fatalities Inhabitants per 10 Million": r_f_per_inhabitat_ten_million,
                    "Road Fatalities Vehicles per 10 Million": r_f_per_vehicle_ten_million,
                    "Road Fatalities Vehicles per 1 Billion": r_f_per_vehicle_one_billion
                })
        except IndexError:
            pass

    filename = f"{output_dir}countries_by_traffic-related_death_rate.csv"
    create_csv(final_data, filename)


if __name__ == "__main__":
    traffic_death_rate()
