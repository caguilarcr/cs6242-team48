import csv
from datetime import date, timedelta
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


DRIVER_PATH = "../helpers/chromedriver"
website_url = 'https://us.trend-calendar.com/trend'
start_date = date(2020, 7, 1)
# end_date = date(2020, 7, 2)
end_date = date(2020, 11, 12)
delta = timedelta(days=1)
max_hashtags = 15


def get_hashtags(url, driver):
    driver.get(url)
    # time.sleep(5)
    twitter_div = driver.find_element_by_id("twitter")
    hashtags = [
        e.find_element_by_tag_name("a").text
        for e in twitter_div.find_elements_by_class_name("readmoretable_line")[:max_hashtags]
    ]
    return hashtags


def store_hashtags(hashtags, output_file="../data/hashtags.csv"):
    with open(output_file, mode='w', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
        for hashtag_date, tags in hashtags.items():
            writer.writerow([hashtag_date] + tags)


def scrape():
    # Selenium config
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    current_date = start_date
    hashtags = {}
    try:
        while current_date <= end_date:
            print(f'Getting tags for {current_date}')
            date_key = current_date.strftime('%Y-%m-%d')
            url = f'{website_url}/{current_date.strftime("%Y-%m-%d")}.html'
            hashtags[date_key] = get_hashtags(url, driver)
            current_date += delta
        driver.quit()
    except BaseException as e:
        print(e)
        driver.quit()
    store_hashtags(hashtags)


if __name__ == '__main__':
    scrape()
