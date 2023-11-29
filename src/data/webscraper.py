import logging
import os
from dotenv import load_dotenv
import MySQLdb
import pandas as pd
from bs4 import BeautifulSoup
from requests import get

load_dotenv()

connection = MySQLdb.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USERNAME"),
    passwd=os.getenv("DATABASE_PASSWORD"),
    db=os.getenv("DATABASE"),
    autocommit=True,
    ssl_mode="VERIFY_IDENTITY",
    ssl={"ca": "cacert-2023-05-30.pem"}
)
cursor = connection.cursor()

def insert_to_database(book: list):
    """
    This function inserts the scraped data to the database
    It takes one argument:
    - book: a list containing the scraped data for one book
    It has no return value
    It inserts the scraped data to the database
    """
    try:
        book[4] = book[4].replace("'", '')
    except Exception as e:
        logging.error(f"Book {book[0]} : {e}")
        book[0] = ""
    try:
        book[4] = book[4].split(',')[0]
    except Exception as e:
        logging.error(f"Book {book[0]} : {e}")
        book[4] = ""
    try:
        book[3] = float(book[3].replace(' AZN', ''))
    except Exception as e:
        logging.error(f"Book {book[0]} : {e}")
        book[3] = -1
    try:
        book[2] = float(book[2])
    except Exception as e:
        logging.error(f"Book {book[0]} : {e}")
        book[2] = -1
    query = f"""INSERT INTO books (book_title, book_rating, book_price, book_authors, book_features, book_cover_url)
                 VALUES ('{book[0]}', {book[2]}, {book[3]}, '{book[4]}', '{book[5]}', '{book[6]}')"""
    cursor.execute(query)
    logging.info(f"Book {book[0]} inserted to database")


class Scraper:
    """
    This class scrapes the data from the website
    It takes two arguments:
    - BASE_URL: the url of the website
    - num_of_pages: the number of pages to scrape
    It has no return value
    It scrapes the data from the website and returns it as a list of lists
    It inserts the scraped data to the database
    """

    def __init__(self, BASE_URL, num_of_pages):
        self.BASE_URL = BASE_URL
        self.num_of_pages = num_of_pages

    def scrape_books(self):
        """
        This method scrapes the data from the website and returns it as a list of lists
        It takes no arguments
        It returns a list of lists containing the scraped data
        It inserts the scraped data to the database
        """

        book_data = []
        # This loop iterates over the number of pages to scrape
        for page_number in range(1, self.num_of_pages + 1):
            url = f'{self.BASE_URL}?page={page_number}'  # This line creates the url for the page to be scraped
            print("URL:" + url)
            response = get(url)  # Get the response from the url
            html_soup = BeautifulSoup(response.text, 'html.parser')  # Parse the response as HTML
            book_containers = html_soup.find_all('div', class_="product-card")  # Find all book containers on the page

            # This loop iterates over each book container on the page
            for container in book_containers:
                # Get the title, description, rating, price, authors, features and cover url of the book
                book_title = container.find('div', class_='product-card-title').get_text(strip=True)

                book_description = container.find('meta', itemprop='description')['content'] if container.find('meta',
                                                                                                               itemprop='description') else None
                book_cover_url = container.find('img', class_='product-card-image')['src'] if container.find('img',
                                                                                                             class_='product-card-image') else None

                book_rating = container.find('meta', itemprop='ratingValue')['content'] if container.find('meta',
                                                                                                          itemprop='ratingValue') else None
                book_price = container.find('div', class_='price in-card').get_text(strip=True)
                book_properties = container.find_all('div', class_='product-card-properties-item')
                book_authors = book_properties[1].get_text(strip=True) if len(book_properties) > 1 else None
                book_features = book_properties[0].get_text(strip=True) if book_properties else None

                # Append the book data to the book_data list
                book = [book_title, book_description, book_rating, book_price, book_authors, book_features,
                        book_cover_url]

                insert_to_database(book)


if __name__ == "__main__":
    logging.basicConfig(filename='scraper.log', level=logging.INFO)
    base_url = 'https://alinino.az/collection/knigi-na-azerbaydzhanskom-yazyke'
    num_pages_for_parse = 89
    cursor.execute("DELETE FROM books;")
    s = Scraper(base_url, num_pages_for_parse)
    s.scrape_books()
