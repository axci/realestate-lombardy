from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from typing import List
import json

from scraper.models import Apartment

class Command(BaseCommand):
    help = 'Load Data'

    def handle(self, *args, **options):
        print('Hello')
        price_from = 10000
        price_to = 1000000
        #www = f'https://www.immobiliare.it/vendita-case/lombardia/?criterio=rilevanza&prezzoMinimo={price_from + 1}&prezzoMassimo={price_to}&noAste=1'
        #soup = self.connect(www)
        
        prices_every_1000 = [price_from]
        price_between = price_from + 1000
        while price_between < price_to:
            prices_every_1000.append(price_between)
            price_between += 1000
        prices_every_1000.append(price_to)
        print(prices_every_1000)

        for i in range(len(prices_every_1000) - 1):
            price_from = prices_every_1000[i]
            price_to = prices_every_1000[i+1]
            www = f'https://www.immobiliare.it/vendita-case/lombardia/?criterio=rilevanza&prezzoMinimo={price_from + 1}&prezzoMassimo={price_to}&noAste=1'
            soup = self.connect(www)


            urls = self.retrieve_urls(soup, www)
            
            counter = 1
            for url in urls:
                try:
                    house_id, title, typology, price, area, link, latitude, longitude, province, city, condition = self.get_dict(url)
                    if isinstance(latitude, (int,float)) and isinstance(longitude, (int,float)) and isinstance(area, (int,float)):
                        Apartment.objects.get_or_create(
                            house_id = house_id,
                            title = title,
                            typology = typology,
                            price = price,
                            area = area,
                            link = link,
                            latitude = latitude,
                            longitude = longitude,
                            province = province,
                            city = city,
                            condition = condition,
                        )
                        print(f"Object {counter} added")
                        counter += 1
                except Exception as e:
                    print(f"With {url} an error ocurred: {e}")


    def connect(self, url):
        """
        Args:
            url (str): The URL to scrape.
        Returns:
            BeautifulSoup: A BeautifulSoup object for the HTML content at the URL.
        """
        resp = requests.get(url)  # Make an HTTP GET request to the URL
        soup = BeautifulSoup(resp.content, "html.parser")  # Create a BeautifulSoup object for the HTML content
        return soup

    def get_number_of_pages(self, soup) -> int:
        """
        Args:
            soup (BeautifulSoup): A BeautifulSoup object for the HTML content.
        
        Returns:
            int: The number of pages for the query.
        """
        try:
            bs_tag = soup.find('script', {'id': '__NEXT_DATA__'})  # Find the script tag with the id '__NEXT_DATA__'
            astring = bs_tag.string  # Extract the string content of the tag
            astring = str(astring)  # Convert the string to a str type
            res = json.loads(astring)  # Load the string as JSON
            
            # Extract the number of pages from the JSON data
            result = res['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['pages'][0]['maxPages']
            
            return result
        
        except (AttributeError, KeyError):
            # handle the exception and return a default value
            return 0

    def retrieve_urls(self, soup, url) -> List[str]:
        """
        Args:
            soup (BeautifulSoup): A BeautifulSoup object for the HTML content.
        
        Returns:
            list: A list of URLs for the houses found.
        """
        try:
            
            number_of_pages = self.get_number_of_pages(soup)  # Get the number of pages
            
            # Find the house links on the first page
            house_cards = soup.find_all('li', class_='nd-list__item in-realEstateResults__item')
            
            # Iterate over the remaining pages
            for page in range(2, number_of_pages + 1):
                #print(page)
                
                soup = self.connect(f'{url}&pag={page}')  # Make an HTTP request to the URL for the page
                
                # Find the house links on the page
                house_cards_add = soup.find_all('li', class_='nd-list__item in-realEstateResults__item')
                house_cards.extend(house_cards_add)  # Add the new house links to the list
            
            print(f'{len(house_cards)} results found')
            
            # Return the list of URLs
            return [house.a['href'] for house in house_cards]
        
        except Exception as e:
            # handle the exception and return an empty list
            return []

    def get_dict(self, house_url):
        soup = self.connect(house_url)
        
        bs_tag = soup.find('script', {'id': 'js-hydration'})  # here is the info about a house
        astring = str(bs_tag.string)  # convert to a str type. The result is a string containg a dictionary
        res = json.loads(astring)  # convert the string to a dictionary
        
        # check area 
        if res['listing']['properties'][0]['surfaceValue'] == '':
            check_area = False
        elif float(res['listing']['properties'][0]['surfaceValue'].split()[0]) < 20:
            check_area = False
        else:
            check_area = True
        
        # if category = Residenziale and area > 20 
        if res['listing']['properties'][0]['category']['name'] == 'Residenziale' and check_area:
            house_id  =  res['listing']['id']
            title     =  res['listing']['title']
            typology  =  res['listing']['properties'][0]['typology']['name']
            price     =  res['listing']['price']['price']   
            area      =  float(res['listing']['properties'][0]['surfaceValue'].split()[0])
            link      =  house_url
            latitude  =  res['listing']['properties'][0]['location']['latitude']
            longitude =  res['listing']['properties'][0]['location']['longitude']
            province  =  res['listing']['properties'][0]['location']['province']['name']
            city      =  res['listing']['properties'][0]['location']['city']['name']

            if res['listing']['properties'][0]['condition'] == None:
                condition = ''
            else:
                condition = res['listing']['properties'][0]['condition']['name']   

        return (house_id, title, typology, price, area, link, latitude, longitude, province, city, condition)


