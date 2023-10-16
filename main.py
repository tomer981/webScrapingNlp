import logging
import json
import os.path
import time
import hashlib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import Config
from article import Article

class Index:
    """
    load const vars from config.yaml file'
    run the function run_bbc every x min
    get all the articles in main page and store and save the articles in data by json and the name is an hash function
    """
    def __init__(self, url, articles_dir):
        self.url = url
        self.articles_dir = articles_dir

    def _save_article(self, article_url):
        hash_article_url = str(hashlib.md5(article_url.encode()).hexdigest())
        if not os.path.isfile('{0}/{1}.{2}'.format(self.articles_dir, hash_article_url, "json")):
            article_web = Article(article_url)
            article_web.article_process()
            if not os.path.exists(self.articles_dir):
                os.makedirs(self.articles_dir)
            with open('{0}/{1}.{2}'.format(self.articles_dir,hash_article_url, "json"), 'w', encoding='utf-8') as f:
                json_string = json.dumps(article_web.__dict__)
                f.write(json_string)
        else:
            logging.info("article: {0} already got processed".format(article_url))

    def run_bbc(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        try:
            # articles = driver.find_elements_by_class_name('block-link__overlay-link')
            articles = driver.find_elements(By.CLASS_NAME, 'block-link__overlay-link')
            for element in articles:
                article_url = element.get_attribute('href')
                try:
                    logging.info("start process article: {0}".format(article_url))
                    self._save_article(article_url)
                except Exception as e:
                    logging.error('error in article: {0}'.format(article_url))
                    logging.exception(e)
                    continue
        finally:
            driver.quit()

    def run(self, func, sec):
        while True:
            sample_time = datetime.today().timestamp()
            func()
            sleep_time = sec - (datetime.today().timestamp() - sample_time)
            if sleep_time > 0:
                time.sleep(sleep_time)


def main(config_path):
    conf = Config.init_by_conf(config_path)
    program = Index(conf.base_url, conf.articles_dir)
    program.run(program.run_bbc, conf.time_interval)


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO,format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",)
    console = logging.StreamHandler(sys.stdout)
    root_logger = logging.getLogger("")
    root_logger.addHandler(console)
    main(sys.argv[1])
