from bs4 import SoupStrainer
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import logging
import os
from csv import writer
from utils import compare_new_and_old_csv, config
from db_api import mongo
logging.basicConfig(level=logging.INFO, filename='log_file', filemode='a', format='%(asctime)s -%(name)s - %(levelname)s - %(message)s',encoding='utf-8',)


class Browser():
    urls=[]
    WITH_ADDITIONAL = ['https://s10.skladchiki.cc/forums/xobbi-i-rukodelie.73/',
                       'https://s10.skladchiki.cc/forums/zdorove.10/',
                       'https://s10.skladchiki.cc/forums/foto.19/', 'https://s10.skladchiki.cc/forums/video.20/']
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument(
            f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
        self.driver = webdriver.Chrome(executable_path=config.driver_path, options=options)
        self.driver.maximize_window()


    def collect_urls(self):

            self.driver.get('https://s10.skladchiki.cc/#skladchikam-kursy.6')
            time.sleep(config.sleep)
            html_source = self.driver.page_source

            only_script = SoupStrainer('div',
                                       {'class': 'block block--category block--category6 collapsible-nodes'})
            soup = BeautifulSoup(html_source, "html.parser", parse_only=only_script)
            headers = soup.find_all("div", {"class": "node-main js-nodeMain"})
            for tag in headers:
                url = 'https://s10.skladchiki.cc' + tag.find('a').attrs['href']
                if url not in Browser.WITH_ADDITIONAL:
                    Browser.urls.append(url)
            logging.info('Url собраны  %s' % len(Browser.urls))

        #collect subUrls
            for i in Browser.WITH_ADDITIONAL:
                self.driver.get(i)
                time.sleep(config.sleep)
                html_source = self.driver.page_source
                soup = BeautifulSoup(html_source, "html.parser",)
                headers = soup.find_all("div", {"class": "node-main js-nodeMain"})
                for tag in headers:
                    url = 'https://s10.skladchiki.cc' + tag.find('a').attrs['href']
                    Browser.urls.append(url)

            logging.info('дополнительные Url собраны')


            add_urls = ['https://s10.skladchiki.cc/forums/muzhskoe-zdorove.94/',
                        'https://s10.skladchiki.cc/forums/diety-i-poxudenie.64/',
                        'https://s10.skladchiki.cc/forums/joga.90/',
                        'https://s10.skladchiki.cc/forums/massazhi.100/',
                        'https://s10.skladchiki.cc/forums/sport-i-trenirovki.65/',
                        'https://s10.skladchiki.cc/forums/drugie-kursy-po-zdorovju.72/',
                        'https://s10.skladchiki.cc/forums/presety-i-ehksheny-dlja-foto.119/',
                        'https://s10.skladchiki.cc/forums/presety-dlja-video.120/',
                        'https://s10.skladchiki.cc/forums/video.20/', 'https://s10.skladchiki.cc/forums/zdorove.10/',
                        'https://s10.skladchiki.cc/forums/foto.19/', 'https://s10.skladchiki.cc/forums/foto.19/']

            #save all urls in file
            for i in add_urls:
                if i not in Browser.urls:
                    Browser.urls.append(i)

            with open('urls_stable_scladchik', 'w', encoding='utf-8') as file:
                for url in Browser.urls:
                    file.write(url)
                    file.write('\n')

    def appent_to_new_staff(self,rows):
        with open(config.file_new_staff_csv, 'a+', newline='', encoding='utf8') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            for i in rows:
                csv_writer.writerow([i])

    def repare_file(self):
        my_dir = config.file_new_staff_csv
        try:
            os.remove(my_dir)
        except:
            pass

    def parsing_process(self):
        with open('urls_stable_scladchik', 'r', encoding='utf-8') as file:
            urls = file.readlines()

        for url in urls:
            url = url.replace('\n','')
            self.driver.get(url)
            time.sleep(config.sleep)
            html_source = self.driver.page_source
            logging.info('url:%s доступ получен ' % url,)#TODO refactor
            soup = BeautifulSoup(html_source, "html.parser", )
            try:
                page_count = soup.find('ul', {'class': 'pageNav-main'})
                page_count.find_all('li')
                page_count = int(page_count.find_all('li').pop().text)
            except:
                page_count = 0
            logging.info('В разделе %s\n%s страниц' % (url, page_count))

            if page_count <= config.page_count_to_parse:
                count = page_count + 1
            else:
                count = config.page_count_to_parse + 1
            for i in range(count):
                i = url + 'page-{}'.format(i)
                print('page: %s,url: %s' % (i, url))
                self.driver.get(i)
                time.sleep(config.sleep)
                html_source = self.driver.page_source
                logging.info('страница:%s доступ получен' % i)#TODO refactor

                logging.info('Парсю %s' % (i))
                soup = BeautifulSoup(html_source, "html.parser")
                rows = []
                topics = soup.find_all('div', {'class': 'structItem-title'})
                for topic in topics:
                    if topic.find("span", string="Доступно"):
                        topic = topic.find('a', {'data-xf-init': 'preview-tooltip'}).text
                        try:
                            mongo.inserting(topic)
                            #rows.append(topic)
                        except:
                            pass

        self.driver.quit()

if __name__ == '__main__':
    browser = Browser()
    if config.collect_urls :
        browser.collect_urls()
    browser.parsing_process()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
