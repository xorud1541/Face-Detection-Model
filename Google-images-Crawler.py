from icrawler.builtin import GoogleImageCrawler
google_crawler = GoogleImageCrawler(storage= {'root_dir': r'./temp'})
google_crawler.crawl(keyword='레드벨벳 조이', max_num=300)