# EXPLORE DATA SET

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_source_url = "https://raw.githubusercontent.com/kolaveridi/kaggle-Twitter-US-Airline-Sentiment-/master/Tweets.csv"
airline_tweets = pd.read_csv(data_source_url)

plot_size = plt.rcParams["figure.figsize"]
plot_size[0] = 8
plot_size[1] = 6
plt.rcParams["figure.figsize"] = plot_size

airline_tweets.airline.value_counts().plot(kind='pie', autopct='%1.0f%%')

airline_tweets.airline_sentiment.value_counts().plot(kind='pie', autopct='%1.0f%%', colors=["red", "yellow", "green"])

airline_sentiment = airline_tweets.groupby(['airline', 'airline_sentiment']).airline_sentiment.count().unstack()
airline_sentiment.plot(kind='bar')

sns.barplot(x='airline_sentiment', y='airline_sentiment_confidence', data=airline_tweets)

plt.show()
