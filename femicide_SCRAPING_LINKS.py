#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import json
import time

browser = wb.Chrome()


# ссылка на 0) федеральные суды 1) приговоры 2) дата поступления 2018-2019 3) по трём нужным статьям - 37843 шт
# вначале ссылки есть аргумент на стартовую позицию и количество документов на странице (макс 20)

url = "https://bsr.sudrf.ru/bigs/portal.html#%7B%22start%22:20,%22rows%22:20,%22uid%22:%221fe4a009-f990-4374-a975-4feaa469b09c%22,%22groups%22:%5B%22Уголовные%20дела%22%5D,%22sorts%22:%5B%7B%22field%22:%22score%22,%22order%22:%22desc%22%7D%5D,%22type%22:%22MULTIQUERY%22,%22multiqueryRequest%22:%7B%22queryRequests%22:%5B%7B%22type%22:%22Q%22,%22request%22:%22%7B%5C%22mode%5C%22:%5C%22EXTENDED%5C%22,%5C%22typeRequests%5C%22:%5B%7B%5C%22fieldRequests%5C%22:%5B%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%201%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20а%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20б%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20в%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20г%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20д%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20е%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20е1%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20ж%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20з%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20и%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20к%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20л%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20м%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20%20п.%20н%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20107%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20107%20%20Часть%201%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20107%20%20Часть%202%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20111%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20111%20%20Часть%204%5C%22,%5C%22sQuery%5C%22:null%7D%5D,%5C%22mode%5C%22:%5C%22AND%5C%22,%5C%22name%5C%22:%5C%22Уголовные%20дела%5C%22,%5C%22typesMode%5C%22:%5C%22AND%5C%22%7D%5D%7D%22,%22operator%22:%22AND%22,%22queryRequestRole%22:%22CATEGORIES%22%7D,%7B%22type%22:%22Q%22,%22request%22:%22%7B%5C%22mode%5C%22:%5C%22EXTENDED%5C%22,%5C%22typeRequests%5C%22:%5B%7B%5C%22name%5C%22:%5C%22common%5C%22,%5C%22mode%5C%22:%5C%22AND%5C%22,%5C%22typesMode%5C%22:%5C%22AND%5C%22,%5C%22fieldRequests%5C%22:%5B%7B%5C%22name%5C%22:%5C%22case_user_document_num%5C%22,%5C%22operator%5C%22:%5C%22GE%5C%22,%5C%22query%5C%22:%5C%221%5C%22%7D%5D%7D%5D%7D%22,%22operator%22:%22AND%22,%22queryRequestRole%22:%22FACET_QUERY###case_user_document_num###Да%22%7D,%7B%22type%22:%22SQ%22,%22queryId%22:%227f9e8ff8-4bc8-46aa-bcbd-f2b3ed5f159f%22,%22operator%22:%22AND%22%7D%5D%7D,%22simpleSearchFieldsBundle%22:null,%22filterGroups%22:%5B%7B%22filterQueries%22:%5B%7B%22field%22:%22case_user_doc_result_date%22,%22query%22:%222018%20год%22,%22not%22:false%7D,%7B%22field%22:%22case_user_document_type%22,%22query%22:%22Приговор%22,%22not%22:false%7D,%7B%22field%22:%22case_user_doc_result%22,%22query%22:%22Вынесен%20ПРИГОВОР%22,%22not%22:false%7D%5D,%22groupMode%22:%22OR%22,%22not%22:false%7D%5D,%22start%22:20%7D"


# In[193]:


import re

def get_id_from_link(link):
    return re.search(r'id=.+?&', link)[0][3:-1]


# In[196]:


def one_page_to_table(page_html):
    df = pd.read_html(page_html)[5]
    soup = BeautifulSoup(page_html)
    urls = [tag.get('href') for tag in soup.find('ul', {'id': 'resultsList'}).find('tbody').find_all('a')]
    df['URL'] = urls
    df['ID'] = df['URL'].apply(get_id_from_link)
    return df


# In[262]:


from math import ceil
n_cases = 21847
n_steps = ceil(n_cases / 20)
n_steps


# In[350]:


#all_data = pd.DataFrame()
curr_position = len(all_data)
for i in range(curr_position, n_cases+1, 20):
    browser.get('http://www.sudrf.ru/')
    url = f"https://bsr.sudrf.ru/bigs/portal.html#%7B%22start%22:{i},%22rows%22:20,%22uid%22:%221fe4a009-f990-4374-a975-4feaa469b09c%22,%22groups%22:%5B%22Уголовные%20дела%22%5D,%22sorts%22:%5B%7B%22field%22:%22score%22,%22order%22:%22desc%22%7D%5D,%22type%22:%22MULTIQUERY%22,%22multiqueryRequest%22:%7B%22queryRequests%22:%5B%7B%22type%22:%22Q%22,%22request%22:%22%7B%5C%22mode%5C%22:%5C%22EXTENDED%5C%22,%5C%22typeRequests%5C%22:%5B%7B%5C%22fieldRequests%5C%22:%5B%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%201%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20а%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20б%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20в%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20г%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20д%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20е%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20е1%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20ж%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20з%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20и%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20к%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20л%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20п.%20м%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20105%20%20Часть%202%20%20п.%20н%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20107%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20107%20%20Часть%201%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20107%20%20Часть%202%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20111%5C%22,%5C%22sQuery%5C%22:null%7D,%7B%5C%22name%5C%22:%5C%22u_case_user_article%5C%22,%5C%22operator%5C%22:%5C%22EX%5C%22,%5C%22query%5C%22:%5C%22Статья%20111%20%20Часть%204%5C%22,%5C%22sQuery%5C%22:null%7D%5D,%5C%22mode%5C%22:%5C%22AND%5C%22,%5C%22name%5C%22:%5C%22Уголовные%20дела%5C%22,%5C%22typesMode%5C%22:%5C%22AND%5C%22%7D%5D%7D%22,%22operator%22:%22AND%22,%22queryRequestRole%22:%22CATEGORIES%22%7D,%7B%22type%22:%22Q%22,%22request%22:%22%7B%5C%22mode%5C%22:%5C%22EXTENDED%5C%22,%5C%22typeRequests%5C%22:%5B%7B%5C%22name%5C%22:%5C%22common%5C%22,%5C%22mode%5C%22:%5C%22AND%5C%22,%5C%22typesMode%5C%22:%5C%22AND%5C%22,%5C%22fieldRequests%5C%22:%5B%7B%5C%22name%5C%22:%5C%22case_user_document_num%5C%22,%5C%22operator%5C%22:%5C%22GE%5C%22,%5C%22query%5C%22:%5C%221%5C%22%7D%5D%7D%5D%7D%22,%22operator%22:%22AND%22,%22queryRequestRole%22:%22FACET_QUERY###case_user_document_num###Да%22%7D,%7B%22type%22:%22SQ%22,%22queryId%22:%227f9e8ff8-4bc8-46aa-bcbd-f2b3ed5f159f%22,%22operator%22:%22AND%22%7D%5D%7D,%22simpleSearchFieldsBundle%22:null,%22filterGroups%22:%5B%7B%22filterQueries%22:%5B%7B%22field%22:%22case_user_doc_result_date%22,%22query%22:%222018%20год%22,%22not%22:false%7D,%7B%22field%22:%22case_user_document_type%22,%22query%22:%22Приговор%22,%22not%22:false%7D,%7B%22field%22:%22case_user_doc_result%22,%22query%22:%22Вынесен%20ПРИГОВОР%22,%22not%22:false%7D%5D,%22groupMode%22:%22OR%22,%22not%22:false%7D%5D,%22start%22:{i}%7D"
    browser.get(url)

    element = WebDriverWait(browser, 25).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#resultViewSelectorOuter > a:nth-child(2)"))
    )
    
    while 'resultHeader' not in browser.page_source:
        time.sleep(0.1)
    time.sleep(5)
    
    browser.find_element_by_css_selector('#resultViewSelectorOuter > a:nth-child(2)').click()
    #resultViewSelectorOuter > a:nth-child(2)


    while 'id="resultsList"' not in browser.page_source:
        time.sleep(0.1)
    time.sleep(1)
    data_per_step = one_page_to_table(browser.page_source)
    all_data = pd.concat([all_data, data_per_step])
    print(f'{len(all_data)}/{n_cases}')
    if len(all_data)%100==0:
        all_data.to_excel('cases_data_no_texts.xlsx')
all_data

