import re
import time
import dateparser
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from google_news_scraper.setting import chrome_option


def __split_google_news_link(url: str) -> tuple[str, str]:
    url_split = re.split(r"start=(\d+)&sa=", url)
    return url_split[0] + 'start=', '&sa=' + url_split[-1]


def __get_google_main_url(url: str) -> str:
    return re.findall(r"^(.*?)(?=&)", url)[0]


def scrape_google_news_link(result_set, number, url):

    url1, url2 = __split_google_news_link(url)
    main_url = __get_google_main_url(url1)
    print(f"\n{main_url}")

    chrome_options = chrome_option()

    driver = webdriver.Chrome(options=chrome_options)
    article_xpath = "//div[contains(@class, 'MjjYud')]/div"

    try:
        for i in range(0, number, 10):
            page = url1 + str(i) + url2
            driver.get(page)
            time.sleep(2)

            articles = driver.find_element(By.XPATH, article_xpath)
            articles = articles.find_elements(By.CLASS_NAME, "SoaBEf")
            print(f"Scraping article {i+1} to {i+10}")

            for article in articles:
                a = article.find_element(By.TAG_NAME, "a").get_attribute("href")
                date = dateparser.parse(
                    date_string = article.find_element(By.CLASS_NAME, "OSrXXb").text,
                    languages=['en', 'id'])
                result_set.add(tuple([a, date.strftime('%Y-%m-%d')]))

    except NoSuchElementException as e:
        print('The pages of the web have run out')

    finally:
        driver.close()
        message = f"Successfully got a total of {len(result_set)} unique article links"
        print(message)
        print('-' * len(message))


def save_link_to_csv(output_file: str, link_set: set, sort: bool = True, asc: bool = False) -> None:

    df = pd.DataFrame(data=link_set, columns=['url', 'date'])
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    if sort:
        df = df.sort_values(by='date', ascending=asc, ignore_index=True)

    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    else:
        df.to_csv(f"{output_file}.csv", index=False)
