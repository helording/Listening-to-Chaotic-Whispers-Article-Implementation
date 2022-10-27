from datetime import datetime
import multiprocessing as mp
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import time
import random
import datetime

#import httplib2

class TimeoutException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

def extraction_wsj(folder, year,nb_days,nb_articles_per_day, links , date, timeout_sec):

    year_str = str(year)
    total = 0
    year_pattern = "http://www.wsj.com/public/page/archive-" +year_str
    article_pattern = 'http://www.wsj.com/articles/'
    article_pattern2 = 'https://www.wsj.com/articles/'

    journal = 'wsj/'
    articles_list = []
    day_count = 0
    articles_count = 0

    for link_d in links:
        print('\n scrapping WSJ for date ; {}\n'.format(date))
        print('total articles scrapped : {} \n'.format(total))
        date_dir = date
        day_path = os.path.join(folder, date_dir)
        if not os.path.exists(day_path):
            os.makedirs(day_path)
        journal_dir = os.path.join(day_path, journal)
        if not os.path.exists(journal_dir):
            os.makedirs(journal_dir)

        try:
            time_start = datetime.datetime.now()
            html_d = urlopen(link_d)
            bs2 = BeautifulSoup(html_d.read(), features="html.parser")
            time_elapsed = datetime.datetime.now() - time_start
            if time_elapsed > timeout_sec:
                raise TimeoutException()

            title = bs2('h1')[0].text + ' '
            title = title.replace("/", " ")
            for tag in bs2():
                del tag['class']
            article = bs2('p')
            del article[0]
            article = [tex.text for tex in article if len(tex.text) > 150]
            text = ''.join([x for x in article])
            text = title + text

            filename = title + '.txt'
            file_path = os.path.join(journal_dir, filename)

            f = open(file_path, 'w')
            f.write(text)
            f.close()

            total = total + 1
        except TimeoutException as e:
            print ("Timeout Exception")
        except Exception as inst:
            print (inst)

    print('Total articles scrapped : {}'.format(total))
    return total


def main():


    timeout_sec = datetime.timedelta(seconds=10)
    start_time = time.time()
    folder = '‎⁨text_data'
    nb_days = 1000
    nb_articles_per_day = 10000
    year_list = [2015]
    month_list = ["08"]
    day_list = ["06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    nb_process = 15
    #day_list = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    nb_process = 15
    day_per_process = int(365 / nb_process)

    for year in year_list:
        for month in month_list:
            for day in day_list:
                successful = False
                while not successful:
                    print("year is: " + str(year))
                    year_str = str(year)
                    date = year_str + "-" + month + "-" + day
                    journal = 'wsj/'
                    html_year = urlopen("https://www.wsj.com/news/archive/" + year_str + month + day)
                    soup = BeautifulSoup(html_year.read(), features="html.parser")
                    year_pattern = "https://www.wsj.com/news/archive/" +  year_str + month + day
                    article_pattern = "https://www.wsj.com/news/archive/" + year_str + month + day
                    article_pattern2 = 'https://www.wsj.com/articles/'

                    #print(soup)

                    links = []
                    preprocessedLinks = []
                    for link in soup.find_all('a'):
                        preprocessedLinks.append(link.get('href'))

                    for link in preprocessedLinks:
                        if link is None:
                            continue
                        elif "articles" not in link:
                            continue
                        elif link in links:
                            print("continuing")
                            continue
                        else:
                            links.append(link)

                    scrapes = extraction_wsj(folder, year, nb_days, nb_articles_per_day, links, date, timeout_sec)

                    if scrapes > 2:
                        successful = True
                    else:
                        successful = False


if __name__ == '__main__':
    main()
