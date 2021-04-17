import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from statistics import mean


def scorer(text):
    return SentimentIntensityAnalyzer().polarity_scores(text)


def remove_stopwords(text):
    words = nltk.word_tokenize(text)
    processed_words = [w for w in words if w not in stopwords]
    processed_words = TreebankWordDetokenizer().detokenize(processed_words)
    return processed_words


df = pd.read_csv(r"C:\Users\Sean Ong\python_basics\fintechnews\fintechnews\fintechnews.csv")
titles = df.iloc[:, 6].values
descs = df.iloc[:, 3].values
stopwords = nltk.corpus.stopwords.words("english")


# analyse title/desc and add scores to new columns
title_scores = []
for title in titles:
    title_score = scorer(str(title))['compound']
    title_scores.append(title_score)
df['title_score'] = title_scores

desc_scores = []
for desc in descs:
    sentence_scores = [scorer(sentence)['compound'] for sentence in nltk.sent_tokenize(desc)]
    desc_score = mean(sentence_scores)
    desc_scores.append(desc_score)
df['desc_score'] = desc_scores


# df.to_csv(r"C:\Users\Sean Ong\python_basics\fintechnews\fintechnews\fintechnews.csv", index=False)



