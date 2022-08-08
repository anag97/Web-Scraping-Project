from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup as soup
import random
import csv

# Use Chrome driver to access web
driver = webdriver.Chrome("C:/Users/AbhikNag97/Downloads/chromedriver_win32/chromedriver.exe")
driver.set_page_load_timeout(30)
driver.get("https://www.academy.com")
driver.implicitly_wait(20)
elems = driver.find_elements_by_xpath("//a[@href]")
n = 20 * 48

# Scraped data will be added to csv file
out_filename = "AcademyData_ProductInfo.csv"

# Create headers for the csv file
headers = "SKU, Category(Level 1), Department(Level 2), Sub-Department(Level 3), Product Name, Original Price, Colors\n"

f = open(out_filename, "w")

f.write(headers)

# Main code for scraping
try:
    for elem in elems:
        url = str(elem.get_attribute("href"))
        sku = str(random.randrange(56896900000, 56897500000, 50000))
        try:
            for i in range(0, n, 48):
                try:
                    strPageNum = str(i)

		    # iterate through all the different urls for the website. 
                    CompleteUrl = (url + "?beginIndex=" + strPageNum)

                    # A lot of sites don't like the user agents of Python 3, so I specify one here
                    req = urllib.request.Request(CompleteUrl, headers={'User-Agent': 'Mozilla/5.0'})

                    html = urllib.request.urlopen(req).read()

                    page_soup = soup(html, "html.parser")

                    containers = page_soup.findAll("div", {"class": "product-info-attributes"})

                    departments = page_soup.findAll("li", {"itemprop": "itemListElement"})

                    department = departments[1].span.text.strip()

                    sub_department = departments[2].span.text.strip()

                    final_department = departments[3].span.text.strip()

		    # Organize extracted data
                    for container in containers:

                        print("SKU: " + sku)
                        print("Department: " + department)
                        print("Sub-Department: " + sub_department)
                        print("Main Department: " + final_department)

                        prod_name = container.h2.text.strip()
                        print("Product Name: " + prod_name)

                        try:
                            price = container.div.span.text.strip()
                            print("Price: " + price)
                        except:
                            price = container.div.text.strip()
                            print("Price: " + price)

                        try:
                            colors_container = container.find("div", {
                                "class": "z-container-flex-no-wrap variant variant-color"})
                            color_container = colors_container.text.strip()
                            print(color_container)
                        except:
                            color_container = "1 color available"
                            print(color_container)

                        print("\n")

                        f.write(sku + "," + department + "," + sub_department + "," + final_department + "," + prod_name.replace("," , " ") + "," + str(price.replace("," , " ")) + "," + str(color_container) + "\n")
                except:
                    break
        except:
            print(" ")
except:
    print("\n")
    print("\n")
    print("Web scraping of website complete!")

f.close()
