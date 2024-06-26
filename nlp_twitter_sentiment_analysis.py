# -*- coding: utf-8 -*-
"""NLP_Twitter_Sentiment_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11yqNsTPDi-bduDM5l8x6w36nD0BK1t6H
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

tweets_df = pd.read_csv('twitter.csv')
tweets_df

tweets_df.info()

tweets_df.describe()

tweets_df['tweet']

tweets_df = tweets_df.drop(['id'], axis=1)

tweets_df.hist(bins=30, figsize=(13,5), color='red')

sns.countplot(tweets_df['label'], label='Count')

tweets_df['length'] = tweets_df['tweet'].apply(len)

tweets_df

tweets_df.describe()

tweets_df[tweets_df['length'] == 11]['tweet']

tweets_df[ tweets_df['length'] == 84 ]['tweet'].iloc[0]

tweets_df['length'].plot(bins = 100, kind='hist')

positive = tweets_df[tweets_df['label']==0]
positive

negative = tweets_df[tweets_df['label']==1]
negative

sentences = tweets_df['tweet'].tolist()
len(sentences)

sentences_as_one_string =" ".join(sentences)
sentences_as_one_string

from wordcloud import WordCloud

plt.figure(figsize=(10,10))
plt.imshow(WordCloud().generate(sentences_as_one_string))

negative_tweets_list = negative['tweet'].tolist()
negative_tweets_str = " ".join(negative_tweets_list)

plt.figure(figsize = (10,10))
plt.imshow(WordCloud().generate(negative_tweets_str))

import string
string.punctuation

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
stopwords.words('english')

from sklearn.feature_extraction.text import CountVectorizer
sample_data = ['This is the first paper.','This paper is the second paper.','And this is the third one.','Is this the first paper?']
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sample_data)

def message_cleaning(message):
    Test_punc_removed = [char for char in message if char not in string.punctuation]
    Test_punc_removed_join = ''.join(Test_punc_removed)

    Test_punc_removed_join_clean = [word for word in Test_punc_removed_join.split() if word.lower() not in stopwords.words('english')]
    return Test_punc_removed_join_clean

tweets_df_clean = tweets_df['tweet'].apply(message_cleaning)
print(tweets_df_clean[5])
print(tweets_df['tweet'][5])

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(analyzer = message_cleaning, dtype = np.uint8)
tweets_countvectorizer = vectorizer.fit_transform(tweets_df['tweet'])

print(vectorizer.get_feature_names_out())

print(tweets_countvectorizer.toarray())

tweets_countvectorizer.shape

X = pd.DataFrame(tweets_countvectorizer.toarray())

X

y = tweets_df['label']

X.shape

y.shape

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2)
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.naive_bayes import MultinomialNB

NB_classifier = MultinomialNB()
NB_classifier.fit(X_train, y_train)

y_predict_test = NB_classifier.predict(X_test)
cm = confusion_matrix(y_test, y_predict_test)
sns.heatmap(cm, annot=True)

print(classification_report(y_test, y_predict_test))

# NOW USING LOGISTIC REGRESSION

import pandas as pd
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Sample Twitter data (replace with your dataset)
data = pd.read_csv('twitter.csv')

# Function to clean and preprocess text data
def clean_text(text):
    # Remove special characters, URLs, and user mentions
    text = re.sub(r'http\S+|www\S+|https\S+|@\w+|#\w+', '', text)

    # Convert text to lowercase
    text = text.lower()

    # Tokenize the text
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Join the cleaned words back into a text
    return ' '.join(words)

# Apply text cleaning and preprocessing to the Twitter data
data['cleaned_text'] = data['tweet'].apply(clean_text)

# Save the cleaned data to a new CSV file
data.to_csv('cleaned_twitter_data.csv', index=False)

# Now you can use 'cleaned_twitter_data.csv' for sentiment analysis

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load your data (replace 'twitter_data.csv' with your dataset)
data = pd.read_csv('cleaned_twitter_data.csv')

# Check for missing values and fill them with an empty string
data['cleaned_text'].fillna('', inplace=True)

# Split the data into train and test sets
X = data['cleaned_text']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data to numerical features using TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust max_features
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Train a logistic regression model
clf = LogisticRegression(C=1.0)
clf.fit(X_train_tfidf, y_train)

# Predict labels on the test set
y_pred = clf.predict(X_test_tfidf)

# Calculate accuracy
acc = accuracy_score(y_test, y_pred)
print('Accuracy:', acc)

from sklearn.metrics import classification_report, confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

import seaborn as sns
sns.heatmap(cm, annot=True)

print(classification_report(y_test, y_pred))