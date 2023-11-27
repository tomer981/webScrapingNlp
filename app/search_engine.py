import json
import glob
import os.path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SearchEngine:
    """
    read all articles files and save the data of each article by url and text,
    transform the text of each article to vector the represent the value, each word show and rarity of the word from the articles
    get a query and check similarity of the words the the exising in each article text,
    sort it from the highest similarity to the smallest and return top 10
    """
    def __init__(self, articles_dir):
        self.tf_idf = None
        self.vectorizer = TfidfVectorizer()
        self.df = pd.DataFrame(columns=['url', 'text'])
        self._initialize(articles_dir)

    def _initialize(self, articles_dir):
        for filename in glob.glob(os.path.join(articles_dir, '*.json')):
            with open(os.path.join(os.getcwd(), filename), 'r') as f:
                article = json.loads(f.read())
                self.df = self.df.append({'url': article['url'], 'text': article['text']}, ignore_index=True)
        self.tf_idf = self.vectorizer.fit_transform(self.df['text'])

    def query(self, query):
        query_vec = self.vectorizer.transform([query])
        results = cosine_similarity(self.tf_idf, query_vec).reshape((-1,))
        self.df['rating'] = results
        self.df = self.df.sort_values(by='rating', ascending=False)
        return self.df.head(10)


if __name__ == '__main__':
    import sys
    article_dir = sys.argv[1]
    query = sys.argv[2]
    search = SearchEngine(article_dir)
    print(search.query(query))
