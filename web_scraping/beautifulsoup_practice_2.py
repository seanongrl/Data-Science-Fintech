# able to connect to mySQL and insert into news and category tables

import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
from unidecode import unidecode


titles = []
descs = []
categories = []
datetimes = []
sources = []
categories_id = []


for page_no in range(1, 3):
    page = requests.get("https://fintechnews.sg/blog/page/" + str(page_no))
    soup = BeautifulSoup(page.content, 'html.parser')

    article_list = soup.find(class_="article-list")

    category = [c.get_text().replace("\n", "") for c in article_list.select(".item-content .content-category")]
    categories.extend(category)

    title = [t.get_text() for t in article_list.select(".item-content .entry-title")]
    titles.extend(title)

    # get read more links to pass into for-loop below
    read_more_links = [r.get("href") for r in article_list.select(".item-content .entry-title a")]

    for link in read_more_links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        # source and datetime
        article_header = soup.find(class_="article-header")
        span = article_header.find("span")

        author = span.findChildren()[1].get_text()
        sources.append(author)

        timestamp = span.findChildren()[2].get_text()
        datetimes.append(timestamp)

        # main article text
        main = soup.find(class_="pf-content")
        words = [x.text for x in main.find_all('p')]
        wordss = [unicodedata.normalize("NFKD", y) for y in words]     # gets rid of weird symbols
        article = unidecode(''.join(wordss))
        descs.append(article)

news = pd.DataFrame({
    "category": categories,
    "title": titles,
    "desc": descs,
    "datetime": datetimes,
    "source": sources})



news.to_csv("fintechscraping.csv")



# connect to database
import mysql.connector

mydb = mysql.connector.connect(
        host="18.139.88.89",
        port="3306",
        user="fintech_user",
        password="fintech_Pass123",
        database="fintech"
)
mycursor = mydb.cursor()

print(mydb)


# insert into category table
category_to_id = {}
for category in categories:
    sql = "SELECT id from category WHERE name='%s'" % category
    mycursor.execute(sql)

    record = mycursor.fetchone()
    if record:
        category_to_id[category] = record[0]  # index 0 corresponds to 'id' column
        categories_id.append(record[0])
    else:
        sql = 'INSERT IGNORE INTO category (name) VALUES (%s)'
        val = (category,)

        mycursor.execute(sql, val)
        mydb.commit()

        last_id = mycursor.lastrowid
        category_to_id[category] = last_id
        categories_id.append(last_id)

print("category was inserted.")


# insert into news table
sql = 'INSERT INTO news (title, description, category_id, dt, source)' \
      'VALUES (%s, %s, %s, %s, %s)' \
      'ON DUPLICATE KEY UPDATE source = source'
val = zip(titles, descs, (category_to_id[category] for category in categories), datetimes, sources)

mycursor.executemany(sql, val)

mydb.commit()

print("news was inserted.")
