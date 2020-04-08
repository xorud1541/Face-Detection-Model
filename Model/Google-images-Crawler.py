from icrawler.builtin import GoogleImageCrawler
import sys

key_word = sys.argv[1]
max_num = int(sys.argv[2])
google_crawler = GoogleImageCrawler(storage= {'root_dir': key_word})
google_crawler.crawl(keyword=key_word, max_num=max_num)