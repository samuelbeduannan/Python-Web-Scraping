import scrapy
from bs4 import BeautifulSoup
import requests
import mechanize
import http.cookiejar as cookielib
import re
import csv
class NewsSpider(scrapy.Spider):

    cook = cookielib.CookieJar()
    req = mechanize.Browser()
    req.set_cookiejar(cook)

    login_url = "https://account.jwnenergy.com/login?pub=DOB_BROWSE&continue=https%3A%2F%2Fwww.dailyoilbulletin.com%2Faccount%2Flogin%2F%3Fcontinue%3Dhttps%253A%252F%252Fwww.dailyoilbulletin.com%252F"
    req.open(login_url)
    req.select_form(nr=0)
    req.form['email'] = '***********'
    req.form['password'] = '********'
    req.submit()

    url = []

    with open("urls.txt", "r") as f:
        urls = f.readlines()
        for url_article in urls:
            url.append(url_article)

    with open("News.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Article Title", "Article Text", "Article Date", "Article Author", "Article Sections", "Article Category", "Article Companies"])

        for link in url:
            article_sections_text = ""
            article_categories_text = ""
            article_companies_text = ""            
            req.open(link)    
            article_text = BeautifulSoup(req.response(), features="lxml").find('div', {"id": "the-body-text"}).text
            article_title = BeautifulSoup(req.response(), features="lxml").title.text
            article_date = BeautifulSoup(req.response(), features="lxml").find('time').text
            article_sections = BeautifulSoup(req.response(), features="lxml").find('ul', {"class": "article-sections"})
            article_categories = BeautifulSoup(req.response(), features="lxml").find('ul', {"class": "article-categories"})
            article_author = BeautifulSoup(req.response(), features="lxml").find('a', itemprop="author")

            if article_author is not None:
                article_author = BeautifulSoup(req.response(), features="lxml").find('a', itemprop="author").text
                print("Article Author: ", article_author)
            else:
                article_author = " "

            article_companies = BeautifulSoup(req.response(), features="lxml").find('ul', {"class": "article-companies"})
            if article_companies is not None:
                for li in article_companies.find_all('li'):
                    print(li.text)
                    if article_companies_text != "":
                        article_companies_text = article_companies_text + ", " + li.text
                    else:
                        article_companies_text = article_companies_text + li.text
            else:
                article_companies_text = " "
            if article_sections is not None:
                for li2 in article_sections.find_all('li'):
                    print(li2.text)
                    if article_sections_text != "":
                        article_sections_text = article_sections_text + ", " + li2.text
                    else:
                        article_sections_text = article_sections_text + li2.text

            else:
                article_sections_text = " "
            if article_categories is not None:
                for li3 in article_categories.find_all('li'):
                    print(li3.text)
                    if article_categories_text != "":
                        article_categories_text = article_categories_text + ", " + li3.text
                    else:
                        article_categories_text = article_categories_text + li3.text

            writer.writerow([article_title, article_text, article_date, article_author, article_sections_text, article_categories_text, article_companies_text])
            print("Article Title: ", article_title)
            print("Article Text: ", article_text)
            print("Article Date: ", article_date)
            print("\n\n\n\n")
         