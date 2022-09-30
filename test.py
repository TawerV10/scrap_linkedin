from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as BS
import csv
import time

def get_html():
    try:
        options = webdriver.ChromeOptions()

        # options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        url = 'https://www.linkedin.com/jobs/search/?currentJobId=3234271550&geoId=101282230&keywords=qa%20tester&location=Germany&refresh=true'
        driver.get(url)

        time.sleep(3)

        blocks = driver.find_elements(By.XPATH, "//ul[@class='jobs-search__results-list']/li/div")
        for i in range(0, len(blocks)):
            action = ActionChains(driver)
            action.move_to_element(blocks[i]).perform()

            blocks[i].click()
            time.sleep(1)

            try:
                name = blocks[i].find_element(By.XPATH, "div[@class='base-search-card__info']/h3").text.strip()
            except:
                name = ''
            try:
                link = blocks[i].find_element(By.XPATH, "a").get_attribute('href').strip()
            except:
                link = ''
            try:
                company_name = blocks[i].find_element(By.XPATH, "div[@class='base-search-card__info']/h4").text.strip()
            except:
                company_name = ''
            try:
                company_link = blocks[i].find_element(By.XPATH, "div[@class='base-search-card__info']/h4/a").get_attribute('href').strip()
            except:
                company_link = ''
            try:
                location = blocks[i].find_element(By.XPATH, "div[@class='base-search-card__info']/div/span").text.strip()
            except:
                location = ''

            try:
                apply_link = driver.find_element(By.XPATH, "//a[@rel='nofollow noopener']").get_attribute('href')
            except:
                apply_link = ''

            try:
                contact = driver.find_element(By.XPATH, "//div[@class='message-the-recruiter message-the-recruiter--jserp']/div/div/a").get_attribute('href')
            except NoSuchElementException:
                contact = ''

            print(f'{i + 1}. {name} - {link} - {company_name} - {company_link} - {location}')
            print(contact, apply_link)

            with open('data.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    name, link, location, company_name, company_link, apply_link, contact
                ])
    except Exception as ex:
        print(ex)
    finally:
        driver.stop_client()
        driver.close()
        driver.quit()

def get_data():
    with open('index.html', encoding='utf-8') as file:
        html = file.read()
        
    soup = BS(html, 'lxml')
    
    all_jobs = soup.find(class_='jobs-search__results-list').find_all('li')
    for job in all_jobs[:25]:
        try:
            name = job.find(class_='base-search-card__info').find('h3').text.strip()
        except:
            name = ''
        try:
            link = job.find('div').find('a').get('href').strip()
        except:
            link = ''
        try:
            company_name = job.find(class_='base-search-card__info').find('h4').text.strip()
        except:
            company_name = ''
        try:
            company_link = job.find(class_='base-search-card__info').find('h4').find('a').get('href').strip()
        except:
            company_link = ''
        try:
            location = job.find(class_='base-search-card__info').find('div').find('span').text.strip()
        except:
            location = ''

        print(f'{name} - {link} - {company_name} - {company_link} - {location}')

def main():
    with open('data.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Position', 'Link', 'Location', 'Company name', 'Company link', 'Apply link', 'Contact person'
        ])

    get_html()

if __name__ == '__main__':
    main()