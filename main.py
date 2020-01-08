import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

project_name = input('Name of project ')
homepage = input('Link of site ')

PROJECT_NAME = project_name
HOMEPAGE = homepage
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 4
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

def crawl():
    queued_lists = file_to_set(QUEUE_FILE)
    if len(queued_lists) > 0:
        print(str(len(queued_lists)) + ' links in the queue')
        create_jobs()

create_workers()
crawl()