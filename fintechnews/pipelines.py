# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import mysql.connector


class FintechnewsPipeline:
    category_to_id = {}
    title_to_id = {}

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host="18.139.88.89",
            port="3306",
            user="fintech_user",
            password="fintech_Pass123",
            database="fintech"
        )
        self.curr = self.conn.cursor(buffered=True)

    def process_item(self, item, spider):
        self.insert_news(item)
        self.insert_category(item)
        self.insert_newscat(item)
        return item

    def insert_news(self, item):
        # check if news entry exists
        sql = "SELECT * FROM news WHERE title='%s'" % item['title']
        self.curr.execute(sql)
        record = self.curr.fetchone()

        if record:
            self.title_to_id[item['title']] = record[0]
        else:
            sql = "INSERT INTO news (title, description, dt, source, image, link)" \
                  "VALUES (%s, %s, %s, %s, %s, %s)" \
                  "ON DUPLICATE KEY UPDATE dt = dt"
            val = (item['title'],
                   item['desc'],
                   item['datetime'],
                   item['source'],
                   item['image'],
                   item['article_link'])

            self.curr.execute(sql, val)
            self.conn.commit()
            self.title_to_id[item['title']] = self.curr.lastrowid

    def insert_category(self, item):
        # check if category exists in database
        sql = "SELECT * FROM categories WHERE name='%s'" % item['category']
        self.curr.execute(sql)
        record = self.curr.fetchone()

        if record:
            self.category_to_id[item['category']] = record[
                0]  # record[0] = category_id
        else:
            sql = "INSERT INTO categories (name) VALUES (%s)"
            val = item['category'],

            self.curr.execute(sql, val)
            self.conn.commit()
            self.category_to_id[item['category']] = self.curr.lastrowid

    def insert_newscat(self, item):
        sql = "INSERT INTO news_categories (news_id, category_id)" \
              "VALUES (%s, %s)" \
              "ON DUPLICATE KEY UPDATE news_id = news_id"
        val = (
        self.title_to_id[item['title']], self.category_to_id[item['category']])

        self.curr.execute(sql, val)
        self.conn.commit()
