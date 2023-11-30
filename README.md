# Web Scraping and Database Insertion Project

## Overview

This project is a web scraping application written in Python that extracts data from a specific website and inserts it into a MySQL database. The scraped data includes book information such as title, description, rating, price, authors, features, and cover URL.

## Features

- **Web Scraping**: Utilizes the BeautifulSoup library to scrape data from the [Alinino](https://alinino.az/collection/knigi-na-azerbaydzhanskom-yazyke) website.
- **MySQL Database Integration**: Uses the MySQLdb library to establish a connection to a MySQL database on [PlanetScale](https://www.planetscale.com/).
- **Data Cleaning**: Cleans and processes scraped data before insertion into the database.
- **Logging**: Implements logging to capture errors and important information during the scraping and database insertion process.

## Prerequisites

- Python 3.x
- Required Python packages: `dotenv`, `MySQLdb`, `pandas`, `bs4` (BeautifulSoup), `requests`

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/arzumanabbasov/ali-and-nino.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:

   ```plaintext
   DATABASE_HOST=your_database_host
   DATABASE_USERNAME=your_database_username
   DATABASE_PASSWORD=your_database_password
   DATABASE=your_database_name
   ```

4. Run the scraper:

   ```bash
   python web_scraper.py
   ```

## Configuration

- **BASE_URL**: The URL of the website to be scraped.
- **num_of_pages**: The number of pages to scrape.

## Database Schema

The scraped data is inserted into a MySQL database table named `books` with the following columns:

- `book_title` (VARCHAR): Title of the book.
- `book_rating` (FLOAT): Rating of the book.
- `book_price` (FLOAT): Price of the book.
- `book_authors` (VARCHAR): Authors of the book.
- `book_features` (VARCHAR): Features of the book.
- `book_cover_url` (VARCHAR): URL of the book cover image.

## Logging

The application logs important information and errors to a file named `scraper.log` for reference.

## License

This project is licensed under the [MIT License](LICENSE).
