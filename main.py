from google_news_scraper.link import scrape_google_news_link
from google_news_scraper.link import save_link_to_csv
from google_news_scraper.content import scrape_news_text
from google_news_scraper.content import save_content_to_csv
from google_news_scraper.content import save_content_to_excel
import pandas as pd

def link():
    result = set()
    url = 'https://www.google.com/search?q=wisata+halal+sumatera+barat&lr=&sca_esv=ea05bd65b2dab007&tbm=nws&sxsrf=ACQVn09EoQ5Z0QWubcVDG0aT83ikFfPDEw:1713157342937&ei=3rQcZvPsOKy7seMPwM-XiA8&start=10&sa=N&ved=2ahUKEwjz0_q2uMOFAxWsXWwGHcDnBfEQ8tMDegQIBBAE&biw=1528&bih=716&dpr=1.25'
    scrape_google_news_link(result, 20, url)
    save_link_to_csv('result.csv', result)

def content():
    news_dict, status_list = scrape_news_text('result.csv', 'id')
    save_content_to_csv('content.csv', news_dict)
    save_content_to_excel('content.xlsx', news_dict)

if __name__ == '__main__':
    content()