from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time


def scrape_forbes_billionaires(url):
    # Make sure the Chrome WebDriver is installed and in your PATH
    driver = webdriver.Chrome()

    driver.get(url)

    # Wait for and click the consent form button
    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.root__OblK1.root__eL_b5'))
        )
        consent_button.click()
    except Exception as e:
        print("Consent button not found or another error occurred:", e)

    # Wait for the scrollable element to be present
    scrollable_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'scrolly-table'))
    )

    # Scroll to the end of the scrollable section
    last_height = driver.execute_script(
        "return arguments[0].scrollHeight", scrollable_element)
    while True:
        driver.execute_script(
            "arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_element)
        time.sleep(0.1)

        new_height = driver.execute_script(
            "return arguments[0].scrollHeight", scrollable_element)
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extracting and storing the data
    billionaires_data = []
    for row in soup.find_all('tr', class_='base ng-scope'):
        # Extract relevant fields
        rank = row.find('td', class_='rank').get_text(strip=True)
        name = row.find('td', class_='name').get_text(strip=True)
        net_worth = row.find('td', class_='Net Worth').get_text(strip=True)
        age = row.find('td', class_='age').get_text(strip=True)
        source = row.find('td', class_='source').get_text(strip=True)
        country = row.find(
            'td', class_='Country/Territory').get_text(strip=True)

        billionaires_data.append([rank, name, net_worth, age, source, country])

    # Save data to a CSV file
    with open('forbes_billionaires_2024.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Name', 'Net Worth',
                        'Age', 'Source', 'Country'])
        writer.writerows(billionaires_data)

    # You can manually close the browser after inspecting
    # driver.quit()


# URL of the Forbes Billionaire 2024 list
url = 'https://www.forbes.com/real-time-billionaires/'  # Replace with the actual URL
scrape_forbes_billionaires(url)
