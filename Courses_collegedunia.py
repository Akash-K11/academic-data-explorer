# Germany Courses

#importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import csv
import concurrent.futures

#setting up headless Firefox browser
firefox_options = Options()
firefox_options.add_argument("--headless")

def scrape_college(element):
    driver = webdriver.Firefox(options=firefox_options)
    soup2 = BeautifulSoup(str(element), "html.parser")
    slug = "https://collegedunia.com" + soup2.find("div", class_ = "jsx-231823654 d-flex align-items-center mb-1 mt-2").find("a")["href"]
    title = soup2.find("div", class_ = "jsx-231823654 d-flex align-items-center mb-1 mt-2").find("a").text
    description = title.split()[0]
    duration = soup2.find("div", class_ = "jsx-231823654 feature feature-duration text-sm text-success d-flex align-items-center font-weight-medium").text
    credits = ""
    university = soup2.find("a", class_ = "jsx-231823654 d-flex align-items-center mb-2").text
    try:
      subject = title.split(']')[-1]
    except:
      subject = ""
    try:
      fee = soup2.find("span", class_ = "jsx-231823654 text-success").text
    except:
      fee = ""
    try:
      eligibility = soup2.find("span", class_ = "jsx-231823654 line-height-19-6").text
    except:
      eligibility = ""
    url = slug
    driver.get(url)
    driver.implicitly_wait(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    field = soup.find("div", class_ ="jsx-4281398864 jsx-4129328768 page-min-height")
    soup2 = BeautifulSoup(str(field), "html.parser")
    try:
        overview = soup2.find("div", class_="jsx-1335585733 jsx-367356671 jsx-1267089218").text
    except (AttributeError, IndexError):
        overview = ""
    try:
      location = soup2.find("span", class_ = "jsx-1056176865 d-block text-md text-capitalize").text
    except (AttributeError, IndexError):
      location = ""
    driver.quit()
    return [title, slug, description, subject, credits, university, location, duration, fee, overview, eligibility]

#initialize list to store job postings
college_list = []

#navigate to the SimplyHired website
url = "https://collegedunia.com/study-abroad/course-finder?country=4"
print("Navigating to", url)
driver = webdriver.Firefox(options=firefox_options)
driver.get(url)
driver.implicitly_wait(10)

print("Scrolling to load all listings...")
old_scroll_height = driver.execute_script("return document.body.scrollHeight")
while True:
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  time.sleep(5)
  new_scroll_height = driver.execute_script("return document.body.scrollHeight")
  if new_scroll_height == old_scroll_height:
    break
  old_scroll_height = new_scroll_height

# #scroll down to load all job listings
# for j in range(10):
#     driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
#     time.sleep(5)

#get HTML source and parse with BeautifulSoup
print("Parsing HTML...")
soup = BeautifulSoup(driver.page_source, "html.parser")
field = soup.find("main", class_ ="jsx-1319606698 col-9 mt-4")
college_elements = field.find_all("div", class_ = "jsx-231823654 card course-card mb-5 p-4 a")
total_listings = len(college_elements)
print("Total listings found:", total_listings)

#quit WebDriver
driver.quit()

# Use multithreading to scrape college data
print("Scraping college data using multithreading...")
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(scrape_college, college_elements)
    for result in results:
        college_list.append(result)
        scraped_count = len(college_list)
        print(f"Scraped {scraped_count} out of {total_listings} listings")

#write data to CSV file
print("Writing data to CSV file...")
with open('Germany_Courses.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    #write header row
    writer.writerow(['Course Name', 'Slug', 'Description', 'Subject', 'Credits', 'University', 'Location', 'Duration', 'Course Fee', 'Course Overview', 'Eligibilty'])
    #write each job posting as a separate row
    for job in college_list:
        writer.writerow(job)

print("CSV file created successfully!")