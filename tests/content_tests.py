import os
import unittest
from numpy import nan
from pandas import read_csv
from pandas import read_excel
from google_news_scraper import scrape_article_content
from google_news_scraper import save_content_to_csv
from google_news_scraper import save_content_to_excel


class ContentTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.link_success = 'data/link_success.csv'
        self.link_failed = 'data/link_failed.csv'
        self.link_no_date = 'data/link_no_date.csv'
        self.link_blocked = 'data/link_blocked.csv'

    def test_scrape_news_text_sce1(self) -> None:
        """Test all links for successful content retrieval"""
        content, status = scrape_article_content(self.link_success, lang='id')
        count_success = 0
        count_failed = 0
        for data in status:
            if data[0] == 'success':
                count_success += 1
            else:
                count_failed += 1
        self.assertEqual(count_success, 10)
        self.assertEqual(count_failed, 0)
        for i in range(len(content)):
            self.assertIsNotNone(content[i]['title'])
            self.assertIsNotNone(content[i]['url'])
            self.assertIsNotNone(content[i]['text'])
            self.assertIsNotNone(content[i]['date'])

    def test_scrape_news_text_sce2(self) -> None:
        """Test not all links for successful content retrieval"""
        content, status = scrape_article_content(self.link_failed, lang='id')
        count_success = 0
        count_failed = 0
        for data in status:
            if data[0] == 'success':
                count_success += 1
            else:
                count_failed += 1
        self.assertLessEqual(count_success, 10)
        self.assertGreaterEqual(count_failed, 0)
        for i in range(len(content)):
            self.assertIsNotNone(content[i]['title'])
            self.assertIsNotNone(content[i]['url'])
            self.assertIsNotNone(content[i]['text'])
            self.assertIsNotNone(content[i]['date'])

    def test_scrape_news_text_no_date(self) -> None:
        """Test all links without date for successful content retrieval"""
        content, status = scrape_article_content(self.link_no_date, lang='id')
        count_success = 0
        count_failed = 0
        for data in status:
            if data[0] == 'success':
                count_success += 1
            else:
                count_failed += 1
        self.assertEqual(count_success, 10)
        self.assertEqual(count_failed, 0)
        for i in range(len(content)):
            self.assertIsNotNone(content[i]['title'])
            self.assertIsNotNone(content[i]['url'])
            self.assertIsNotNone(content[i]['text'])
            self.assertIsNone(content[i]['date'] if content[i]['date'] else None)

    def test_scrape_news_text_blocked(self) -> None:
        """Test all links getting blocked for content retrieval"""
        _, status = scrape_article_content(self.link_blocked, lang='id')
        count_success = 0
        count_failed = 0
        for data in status:
            if data[0] == 'success':
                count_success += 1
            else:
                count_failed += 1
        self.assertLessEqual(count_success, 6)
        self.assertGreaterEqual(count_failed, 0)

    def test_save_content_to_csv(self) -> None:
        """Test save scraping results to CSV file"""
        csv_file = 'test.csv'
        content, _ = scrape_article_content(self.link_success, lang='id')
        save_content_to_csv(csv_file, content)

        df_content = read_csv(csv_file, sep=';')
        df_content.replace(nan, None, inplace=True)
        for i in range(len(content)):
            self.assertEqual(df_content.loc[i, 'title'], content[i]['title'])
            self.assertEqual(df_content.loc[i, 'url'], content[i]['url'])
            self.assertEqual(df_content.loc[i, 'text'], content[i]['text'])
            self.assertEqual(df_content.loc[i, 'date'], content[i]['date'])
            self.assertEqual(df_content.loc[i, 'tags'], content[i]['tags'] if content[i]['tags'] else None)

        os.remove('test.csv')

    def test_save_content_to_excel(self) -> None:
        """Test save scraping results to CSV file"""
        excel_file = 'test.xlsx'
        content, _ = scrape_article_content(self.link_success, lang='id')
        save_content_to_excel(excel_file, content)

        df_content = read_excel(excel_file)
        df_content.replace(nan, None, inplace=True)
        for i in range(len(content)):
            self.assertEqual(df_content.loc[i, 'title'], content[i]['title'])
            self.assertEqual(df_content.loc[i, 'url'], content[i]['url'])
            self.assertEqual(df_content.loc[i, 'text'], content[i]['text'])
            self.assertEqual(df_content.loc[i, 'date'], content[i]['date'])
            self.assertEqual(df_content.loc[i, 'tags'], content[i]['tags'] if content[i]['tags'] else None)

        os.remove('test.xlsx')


if __name__ == '__main__':
    unittest.main()
