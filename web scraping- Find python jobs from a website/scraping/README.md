**Title: Web Scraping-find python related jobs from a website

## Introduction
This Python script is designed to scrape data from a website containing jobs in the "PYTHON" category and create a txt file for further manipulation and preprocessing. It utilizes the `requests`and `BeautifulSoup`  libraries for web scraping.

## Requirements
- Python 3.x
- requests library
- BeautifulSoup library

## Installation
1. Ensure you have Python 3.x installed on your system. If not, download it from the official Python website (https://www.python.org/downloads/) and install it.
2. Install the required libraries by running the following commands in your terminal or command prompt:
```
pip install requests
pip install beautifulsoup4
```

## How to Use
1. Clone or download the script from the GitHub repository (provide GitHub repository link here).
2. Open the script using your favorite Python IDE or text editor.
3. Modify the `url` variable in the script to point to the starting page of the "Mystery" books category you want to scrape.
4. Run the script. It will scrape data from multiple pages of the category and store it in a DataFrame.
5. The resulting DataFrame will contain information about book titles, prices, and star ratings.

## Usage Example
```python
import requests
from bs4 import BeautifulSoup
