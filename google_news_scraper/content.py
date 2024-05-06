import time
import pandas as pd

from newspaper import Article
from selenium import webdriver
from google_news_scraper.setting import chrome_option


def scrape_news_text(input_csv: str, lang: str = 'id') -> tuple[dict, list]:

    df_news_link = pd.read_csv(input_csv)
    dict_news = dict()
    status = list()

    for i in df_news_link.index:

        article = Article(str(df_news_link['url'][i]), language=lang)

        for trial_number in range(1, 3):
            if trial_number == 1:
                article.download()
                if article.download_state != 2:
                    continue
            else:
                chrome_options = chrome_option()
                driver = webdriver.Chrome(options=chrome_options)
                try:
                    driver.get(str(df_news_link['url'][i]))
                    input_html = driver.page_source
                    time.sleep(2)
                    article.download(input_html)
                except Exception as e:
                    pass
                finally:
                    driver.close()
            try:
                article.parse()
                # Jika teks tidak kosong, ambil isinya
                if article.text:
                    print(f"{i + 1} [success] {article.url}")
                    status.append('success')
                    dict_news[i] = {
                        'title': str(article.title),
                        'url': str(article.url),
                        'text': str(article.text),
                        'date': df_news_link['date'][i],
                        'tags': ', '.join(article.tags)
                    }
                    break
                if trial_number == 1:
                    continue
            except Exception as e:
                pass

            # jika HTML atau teks nya kosong maka FAILED
            print(f"{i + 1} [failed ] {article.url}")
            status.append('failed')

    df_status = pd.DataFrame(status, columns=['status'])
    print(df_status['status'].value_counts())

    return dict_news, status


def save_content_to_csv(output_file: str, content_dict: dict) -> None:
    df_news = pd.DataFrame.from_dict(content_dict, orient='index')
    if output_file.endswith('.csv'):
        df_news.to_csv(output_file, index=False, sep=";")
    else:
        df_news.to_csv(f"{output_file}.csv", index=False, sep=";")


def save_content_to_excel(output_file: str, content_dict: dict) -> None:
    df_news = pd.DataFrame.from_dict(content_dict, orient='index')
    if output_file.endswith('.xlsx'):
        df_news.to_excel(output_file)
    else:
        df_news.to_excel(f"{output_file}.xlsx")
