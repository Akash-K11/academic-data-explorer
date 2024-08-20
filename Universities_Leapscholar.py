# USA Universities 2nd part

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
import pandas as pd

#setting up headless Firefox browser
firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)

# Read the CSV file into a DataFrame
file_path = '/content/USA_Universities.csv'
df = pd.read_csv(file_path, encoding='latin-1')
# Assume the column with URLs is named 'url_column'
url_column = df['University Link']
print(len(url_column))
college_list = []

# Iterate over the URLs
for count, url in enumerate(url_column):
      print(count)
      driver.get(url)
      # print(driver)
      driver.implicitly_wait(1)

      for j in range(1):
          driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
          time.sleep(1)

      #get HTML source and parse with BeautifulSoup
      soup = BeautifulSoup(driver.page_source, "html.parser")
      description = ""
      try:
        des_list = soup.find("div", class_ = "jsx-9bf980a20a702a82 leading-6 text-base text-[#667085] scrollbar-hide").find("div").find_all("p")
        for ele in des_list:
          description += ele.text
      except:
        description = ""
      try:
        banner = "https://leapscholar.com" + soup.find("img", alt = "University cover image")["src"]
      except:
        banner = ""
      try:
        logo_url = "https://leapscholar.com" + soup.find("img", alt = "University logo")["src"]
      except:
        logo_url = ""
      url = url + "/programs"
      driver.get(url)
      driver.implicitly_wait(1)
      for k in range(1):
        driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
        time.sleep(1)
      soup = BeautifulSoup(driver.page_source, "html.parser")
      try:
        courses_list = soup.find_all("div", class_ = "p-3 md:p-4 border md:w-[calc(50%-16px)] justify-between border-[#E8E8E8] flex flex-col gap-4 rounded-md shadow-[0px_4px_8px_rgba(67,54,149,0.08)]")
        courses = ""
        for course_count, ele in enumerate(courses_list):
          courses += f'{course_count + 1}) {ele.text}\n'
      except:
        courses = ""
      college_list.append([description, banner, logo_url, courses])

#quit WebDriver
driver.quit()

#write data to CSV file
with open('USA_Universities 2nd part.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    #write header row
    writer.writerow(['Description', 'Banner', 'University Logo', 'Courses'])
    #write each job posting as a separate row
    for job in college_list:
        writer.writerow(job)

print("CSV file created successfully!")