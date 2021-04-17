import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

df = pd.read_csv(r"C:\Users\Sean Ong\python_basics\fintechnews\fintechnews\fintechnews.csv")
titles = df['title']

count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')  # instance of countvectorizer
doc_term_matrix = count_vect.fit_transform(titles.values.astype('U'))

LDA = LatentDirichletAllocation(n_components=10, random_state=42)  # n_components = no. of topics
LDA.fit(doc_term_matrix)

topic_probabilities = LDA.transform(doc_term_matrix)  # This method will assign the probability of all the topics to each document.
                                                      # Each of the document has 5 columns where each column corresponds to the probability value of a particular topic.
topic_indexes = topic_probabilities.argmax(axis=1)    # topic with the highest probability

topic_words_list = []
for index in topic_indexes:
    topic = LDA.components_[index]
    topic_words = [count_vect.get_feature_names()[i] for i in topic.argsort()[-5:]]  # top 5 words for each topic
    topic_words_list.append(topic_words)                                             # list of top 5 words for each news

df['topic'] = topic_indexes
df['top words'] = topic_words_list

print(df.iloc[:, 7:])





