from __future__ import absolute_import, unicode_literals
from celery import shared_task

from app.scraping.cos_scraping import scraping

@shared_task(name='scraping.add')
def scraping_scheduling():
    sc = scraping(1)

# 이건 시험용
#@shared_task(name='hello.add')
#def hello():
#    print('hello')