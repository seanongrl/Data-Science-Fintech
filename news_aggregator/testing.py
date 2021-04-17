from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import create_session
from sqlalchemy.ext.automap import automap_base


engine = create_engine("mysql+mysqlconnector://fintech_user:fintech_Pass123@18.139.88.89/fintech")

Base = automap_base()
Base.prepare(engine, reflect=True)

session = create_session(bind=engine)

News = Base.classes.news_categories
print(News)


