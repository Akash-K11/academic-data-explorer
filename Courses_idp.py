import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Function to scrape a single page
def scrape_page(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    print(f"Scraping URL: {url}")
    driver.get(url)
    driver.implicitly_wait(1)

    # Scroll down to load all job listings
    for j in range(1):
        driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    field = soup.find("ul", class_="product__listing product__list sr_prod")
    college_elements = field.find_all("li", class_="product__list--item green-image-effect")

    college_list = []

    for element in college_elements:
        soup2 = BeautifulSoup(str(element), "html.parser")
        subject = "Computing and IT" if "computing-and-it" in url else "Engineering"
        slug = "https://www.idp.com" + soup2.find("a")["href"]
        title = soup2.find("a", class_="product__list--name").text
        description = soup2.find("div", class_="qualification").find_all("p")[1].text
        credits = ""
        try:
            eligibility = soup2.find("div", class_="turn-around").find_all("p")[1].text
        except:
            eligibility = ""
        university = soup2.find("div", class_="insti_cntry").find("a").text
        location = soup2.find("div", class_="media-body").text
        try:
            fee = soup2.find("div", class_="score").find_all("p")[1].text
        except:
            fee = ""

        driver.get(slug)
        driver.implicitly_wait(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        field = soup.find("div", class_="main-content-wrapper")
        soup2 = BeautifulSoup(str(field), "html.parser")
        try:
            overview = soup2.find("div", class_="insti_abt_cont").text
        except (AttributeError, IndexError):
            overview = ""
        try:
            duration = ""
            duration_list = soup2.find_all("div", class_="count_cnt")
            for ele in duration_list:
                if ele.find("img")["src"] == "/_ui/responsive/common/images/time-outline.svg":
                    duration = ele.find("p").text
                    break
        except (AttributeError, IndexError):
            duration = ""

        college_list.append([title, slug, description, subject, credits, university, location, duration, fee, overview, eligibility])

    driver.quit()
    print(f"Completed scraping URL: {url}")
    return college_list

# Function to gather all URLs
def gather_urls(base_url, pages):
    urls = []
    for i in range(pages):
        urls.append(base_url + str(i))
    return urls

# Main scraping function
def main():
    base_urls = [
        "https://www.idp.com/india/search/computing-and-it/?q=:popularity:destination:United+States&page=",
        "https://www.idp.com/india/search/engineering/?q=:popularity:destination:United+States&page="
    ]
    pages = [639, 966]

    all_urls = []
    for base_url, page_count in zip(base_urls, pages):
        all_urls.extend(gather_urls(base_url, page_count))

    total_urls = len(all_urls)
    print(f"Total URLs to scrape: {total_urls}")

    college_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(scrape_page, all_urls)

        for i, result in enumerate(results, start=1):
            college_list.extend(result)
            print(f"Progress: {i}/{total_urls} URLs scraped")

    # Write data to CSV file
    with open('USA_Courses.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Course Name', 'Slug', 'Description', 'Subject', 'Credits', 'University', 'Location', 'Duration', 'Course Fee', 'Course Overview', 'Eligibility'])
        for college in college_list:
            writer.writerow(college)

    print("CSV file created successfully!")

if __name__ == "__main__":
    main()
