from app import app
from app.models import News, Category, NewsCategory
from flask import render_template, flash, redirect, url_for, request


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    articles = News.query\
        .join(NewsCategory, News.news_id == NewsCategory.news_id)\
        .join(Category, NewsCategory.category_id == Category.category_id)\
        .add_columns(News.title, News.source, News.link, News.dt, Category.name)\
        .order_by(News.dt.desc())\
        .paginate(page, 5, False)
    next_url = url_for('index', page=articles.next_num) \
        if articles.has_next else None
    prev_url = url_for('index', page=articles.prev_num) \
        if articles.has_prev else None
    return render_template('index.html', title='Financial News Aggregator', articles=articles.items,
                           next_url=next_url,
                           prev_url=prev_url)


