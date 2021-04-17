import schedule
import time
from datetime import datetime
import os


def job():
    os.system('scrapy crawl fintechnewssg')
    os.system('scrapy crawl finextra')
    os.system('scrapy crawl cnbc')
    os.system('scrapy crawl cnbc2')
    os.system('scrapy crawl reuters')



job()
schedule.every().hour.do(job)
print('Scheduler initialised at ' + str(datetime.now()))
print('Next job is set to run at: ' + str(schedule.next_run()))

while True:
    schedule.run_pending()
    time.sleep(900)  # 15min
    print('Next job is set to run at: ' + str(schedule.next_run()))
