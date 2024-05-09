import os
import csv
import unittest
from google_news_scraper import save_link_to_csv
from google_news_scraper import scrape_google_news_link


class LinkTestCase(unittest.TestCase):

    def setUp(self):
        self.result = set()
        self.url = 'https://www.google.com/search?q=indonesia&sca_esv=74c740cd3a771c52&tbm=nws&prmd=nimvsbtz&sxsrf=ADLYWILWlzoVWC2mq7FqKBwxDoDLbr_t2A:1715189889486&ei=gbg7ZqGYHeKf4-EPxNOb6Ak&start=10&sa=N&ved=2ahUKEwjh3NagzP6FAxXizzgGHcTpBp0Q8tMDegQIBBAE&biw=1528&bih=716&dpr=1.25'

    def test_scrape_google_news_link_sce1(self):
        """Scraping 0 link"""
        result_status = scrape_google_news_link(self.result, self.url, 0)
        self.assertFalse(result_status)

    def test_scrape_google_news_link_sce2(self):
        """Scraping -5 link"""
        result_status = scrape_google_news_link(self.result, self.url, -5)
        self.assertFalse(result_status)

    def test_scrape_google_news_link_sce3(self):
        """Scraping 5 link"""
        result_status = scrape_google_news_link(self.result, self.url, 5)
        self.assertTrue(result_status)
        self.assertEqual(len(self.result), 5)

    def test_scrape_google_news_link_sce4(self):
        """Scraping 35 link"""
        result_status = scrape_google_news_link(self.result, self.url, 35)
        self.assertTrue(result_status)
        self.assertEqual(len(self.result), 35)

    def test_scrape_google_news_link_sce5(self):
        """Scraping 1000 link (usually it is impossible to get 1000)"""
        result_status = scrape_google_news_link(self.result, self.url, 1000)
        self.assertTrue(result_status)
        self.assertLessEqual(len(self.result), 1000)

    def test_save_to_csv(self):
        """Test save scraping results to CSV file"""
        csv_file = 'test.csv'
        scrape_google_news_link(self.result, self.url, 5)
        save_link_to_csv(csv_file, self.result, True, False)

        link_list = list()
        for url, date in self.result:
            link_list.append(url)

        with open(csv_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            self.assertEqual(next(reader), ['url', 'date'])
            for i in range(len(self.result)):
                self.assertTrue(next(reader)[0] in link_list)

        os.remove('test.csv')


if __name__ == '__main__':
    unittest.main()
