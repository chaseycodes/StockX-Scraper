# StockX Scraper
A program to scrape **every** sneaker on StockX! 

## About
> I wrote this program to scrape data for my sneaker application, Venture Kicks! Check it out when you have the chance :)

## Dependencies
```python
pip3 install bs4
pip3 install urllib
pip3 install requests
pip install selenium
```

## How To
1. URL-Scraper: Will return every sneaker's URL and Image URL as a json file.
2. Sneaker-Scraper: Using the file from URL-Scraper, Sneaker-Scraper will open each individual page and return its data into a new json file. 
3. Image-Downloader: Using the files from Sneaker-Scraper, Image-Downloader will save each sneaker image into static.
> DISCLAIMER: Due to amount of time it takes to complete, it is intentionally written as separate programs to save progress and avoid restart. 

## Run - [from root folder]
```python
python3 1-url_scraper.py
python3 2-sneaker_scraper.py
python3 3-image_downloader.py
```

