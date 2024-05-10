import re
import time
import dateparser
from pandas import DataFrame
from pandas import to_datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from google_news_scraper.setting import chrome_option


def __split_google_news_link(url: str) -> tuple[str, str]:
    """
    Split the Google News link right at the page number.

    Args:
        url (str): Google News link

    Returns:
        tuple[str, str]: (first_url, second_url)
    """
    url_split = re.split(r"start=(\d+)&sa=", url)
    first_url = url_split[0] + 'start='
    second_url = '&sa=' + url_split[-1]
    return first_url, second_url


def __get_google_main_url(url: str) -> str:
    """
    Get Google News domain name and main parameters.

    Args:
        url (str): Google News link

    Returns:
        str: main_url
    """    
    main_url = re.findall(r"^(.*?)(?=&)", url)[0]
    return main_url


def scrape_google_news_link(result_set: set, url: str, number: int = 100) -> bool:
    """
    Scraping links in the given Google News ``url``, a number of ``number`` links, to be stored in ``result_set``.

    - You can use the same ``result_set`` to scrape links from several Google News links.
    - For a large target ``number``, for example 1000 links, there is no guarantee that you will get 1000 links. It all depends on the number of results displayed by Google News.

    Args:
        result_set (set): Set to save the results of link scraping in Google News
        url (str): Google News link
        number (int, optional): Total links that you want to scrape. Defaults to 100.

    Returns:
        bool
    """
    if number < 1:
        print('\ntarget number must be > 0')
        return False

    target = len(result_set) + number
    url1, url2 = __split_google_news_link(url)
    main_url = __get_google_main_url(url1)
    print(f"\n{main_url}")

    chrome_options = chrome_option()

    driver = webdriver.Chrome(options=chrome_options)
    article_xpath = "//div[contains(@class, 'MjjYud')]/div"

    try:
        for i in range(0, 1000, 10):
            page = url1 + str(i) + url2
            driver.get(page)
            time.sleep(2)

            articles = driver.find_element(By.XPATH, article_xpath)
            articles = articles.find_elements(By.CLASS_NAME, "SoaBEf")
            print(f"Scraping article {i+1} to {i+10}")

            for article in articles:
                a = article.find_element(By.TAG_NAME, "a").get_attribute("href")
                date = dateparser.parse(
                    date_string=article.find_element(By.CLASS_NAME, "OSrXXb").text,
                    languages=['en', 'id'])
                result_set.add(tuple([a, date.strftime('%Y-%m-%d')]))
                if len(result_set) == target:
                    break
            if len(result_set) == target:
                break
    except NoSuchElementException as e:
        print('The pages of the web have run out')
    finally:
        driver.close()

    message = f"Successfully got a total of {len(result_set)} unique article links"
    print(message)
    print('-' * len(message))
    return True


def save_link_to_csv(output_file: str, link_set: set, sort: bool = True, asc: bool = False) -> None:
    """
    Converts ``result_set`` results from ``scrape_google_news_link()`` to a CSV file.

    Args:
        output_file (str): The desired output CSV file name
        link_set (set): set of link scraping results
        sort (bool, optional): Data is sorted by date. Defaults to True.
        asc (bool, optional): Data is sorted by date in ascending order. Defaults to False.
    """    
    df = DataFrame(data=link_set, columns=['url', 'date'])
    df['date'] = to_datetime(df['date'], format='%Y-%m-%d')

    if sort:
        df = df.sort_values(by='date', ascending=asc, ignore_index=True)

    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    else:
        df.to_csv(f"{output_file}.csv", index=False)
