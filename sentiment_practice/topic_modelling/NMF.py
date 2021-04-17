import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

df = pd.read_csv(r"C:\Users\Sean Ong\python_basics\fintechnews\fintechnews\fintechnews.csv")
titles = df['title']

tfidf_vect = TfidfVectorizer(max_df=0.8, min_df=2, stop_words='english')  # instance of countvectorizer
doc_term_matrix = tfidf_vect.fit_transform(titles.values.astype('U'))

nmf = NMF(n_components=10, random_state=42)
nmf.fit(doc_term_matrix)

topic_probabilities = nmf.transform(doc_term_matrix)
topic_indexes = topic_probabilities.argmax(axis=1)

topic_words_list = []
for index in topic_indexes:
    topic = nmf.components_[index]
    topic_words = [tfidf_vect.get_feature_names()[i] for i in topic.argsort()[-5:]]
    topic_words_list.append(topic_words)

df['topic'] = topic_indexes
df['top words'] = topic_words_list

print(df.iloc[:, 7:])





