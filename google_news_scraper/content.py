import time
from pandas import read_csv
from pandas import DataFrame
from newspaper import Article
from selenium import webdriver
from google_news_scraper.setting import firefox_option


def scrape_news_text(csv: str, lang: str = 'id') -> tuple[dict, list]:
    """
    Retrieves ``lang`` language content from all links in ``link_csv``.

    Args:
        csv (str): The CSV file name contains all the scraped links from Google News
        lang (str, optional): _The language of the article link to be extracted. Defaults to 'id'.

    Returns:
        tuple[dict, list]: (dict_news, status)
    """    
    df_news_link = read_csv(csv)
    date_status = 'date' in df_news_link.columns
    dict_news = dict()
    status = list()
    number = -1
    print()

    for i in df_news_link.index:

        article = Article(str(df_news_link['url'][i]), language=lang)

        for trial_number in range(1, 3):
            if trial_number == 1:
                article.download()
                if article.download_state != 2:
                    continue
            else:
                firefox_options = firefox_option()
                driver = webdriver.Chrome(options=firefox_options)
                try:
                    driver.get(str(df_news_link['url'][i]))
                    time.sleep(2)
                    input_html = driver.page_source
                    article.download(input_html)
                except Exception as e:
                    pass
                finally:
                    driver.close()
            try:
                article.parse()
                if article.text and not article.title.startswith('Attention Required!'):
                    number += 1
                    dict_news[number] = {
                        'title': str(article.title),
                        'url': str(article.url),
                        'text': str(article.text),
                        'date': df_news_link['date'][i] if date_status else '',
                        'tags': ', '.join(article.tags)
                    }
                    print(f"{i + 1} [success] {article.url}")
                    status.append(['success', str(df_news_link['url'][i])])
                    break
                if trial_number == 1:
                    continue
            except Exception as e:
                pass

            print(f"{i + 1} [failed ] {article.url}")
            status.append(['failed', str(df_news_link['url'][i])])

    count_success = 0
    count_failed = 0
    for data in status:
        if data[0] == 'success':
            count_success += 1
        else:
            count_failed += 1

    print('status')
    print(f"success\t{count_success}")
    print(f"failed\t{count_failed}")

    return dict_news, status


def save_content_to_csv(output_file: str, content_dict: dict) -> None:
    """
    Converts ``dict_news`` results from ``scrape_news_text()`` to a CSV file.

    Args:
        output_file (str): The desired output CSV file name
        content_dict (dict): Dictionary of content scraping results
    """    
    df_news = DataFrame.from_dict(content_dict, orient='index')
    if output_file.endswith('.csv'):
        df_news.to_csv(output_file, index=False, sep=";")
    else:
        df_news.to_csv(f"{output_file}.csv", index=False, sep=";")


def save_content_to_excel(output_file: str, content_dict: dict) -> None:
    """
    Converts ``dict_news`` results from ``scrape_news_text()`` to a XLSX file.

    Args:
        output_file (str): The desired output XLSX file name
        content_dict (dict): Dictionary of content scraping results
    """    
    df_news = DataFrame.from_dict(content_dict, orient='index')
    if output_file.endswith('.xlsx'):
        df_news.to_excel(output_file, index=False)
    else:
        df_news.to_excel(f"{output_file}.xlsx", index=False)
