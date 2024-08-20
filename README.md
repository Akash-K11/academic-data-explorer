# University and Course Scraper

## Description
This repository contains a collection of Python scripts that can be used to scrape university and course information from various websites, including Leapscholar, CollegeDunia and IDP.

## Features
- Scrapes university information such as name, country, region, fees, ranking, establishment year, logo, and more.
- Scrapes course information such as course name, description, banner, logo, and list of courses offered.
- Supports scraping data from multiple pages and pages.
- Writes the scraped data to CSV files.

## Requirements
- Python 3.x
- The following Python packages:
  - `selenium`
  - `bs4` (BeautifulSoup)
  - `time`
  - `csv`
  - `pandas` (for the USA Universities 2nd part script)

## Usage
1. Install the required packages by running `pip install -r requirements.txt`.
2. Update the script files with the desired URLs, page ranges, and other parameters as needed.
3. Run the individual script files using `python <script_name>.py` or `python <notebook_name>.ipynb`.
4. The scraped data will be saved to CSV files in the same directory as the script files.

## Scripts
1. `Courses_collegedunia.py`: Scrapes course information from CollegeDunia for a country.
2. `Courses_idp.py`: Scrapes course information from IDP for a country.
3. `Universities_collegedunia.ipynb`: Scrapes university information from CollegeDunia for a country.
4. `Universities_Leapscholar.py`: Scrapes additional university information from the Universities dataset.