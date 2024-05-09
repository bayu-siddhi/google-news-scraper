import os
import unittest
from numpy import nan
from pandas import read_csv
from pandas import read_excel
from google_news_scraper import scrape_news_text
from google_news_scraper import save_content_to_csv
from google_news_scraper import save_content_to_excel


class ContentTestCase(unittest.TestCase):

    def test_scrape_news_text_sce1(self):
        """Test all links for successful content retrieval"""
        content, status = scrape_news_text('link_success.csv', lang='id')
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

    def test_scrape_news_text_sce2(self):
        """Test not all links for successful content retrieval"""
        content, status = scrape_news_text('link_failed.csv', lang='id')
        count_success = 0
        count_failed = 0
        for data in status:
            if data[0] == 'success':
                count_success += 1
            else:
                count_failed += 1
        self.assertLess(count_success, 10)
        self.assertGreater(count_failed, 0)
        for i in range(len(content)):
            self.assertIsNotNone(content[i]['title'])
            self.assertIsNotNone(content[i]['url'])
            self.assertIsNotNone(content[i]['text'])
            self.assertIsNotNone(content[i]['date'])

    def test_save_content_to_csv(self):
        """Test save scraping results to CSV file"""
        csv_file = 'test.csv'
        content, status = scrape_news_text('link_success.csv', lang='id')
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

    def test_save_content_to_excel(self):
        """Test save scraping results to CSV file"""
        excel_file = 'test.xlsx'
        content, status = scrape_news_text('link_success.csv', lang='id')
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
