import heapq
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from nltk import FreqDist
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from selenium import webdriver

class Article:
    """
    get the article url,
    take the text,
    clean the text from stop words and unwanted chars,
    define each word by frequency of uses by max word frequency,
    summarize:
    take the text and split it to sentences,
    define each sentence by score of frequencies of the words
    summary is the combinations of sentences with less than 100 word with max value,
    sentiment:
    analyze the word in the text by the positive, negative, and neutral and save it sentiment
    """
    def __init__(self, url):
        self.url = url
        self.text = ''
        self.summary = None
        self.sentiment = None

    def _clean_txt(self, text):
        text = re.sub(r'#', '', text)
        text = re.sub(r',', '', text)
        text = re.sub(r':', '', text)
        text = re.sub(r'`', '', text)
        text = re.sub(r'’', '', text)
        text = re.sub(r'"', '', text)
        return text

    def _calc_sentiment(self):
        analyzer = SentimentIntensityAnalyzer()
        self.sentiment = analyzer.polarity_scores(self.text)

    def _text_to_token_words(self):
        tokens = self._clean_txt(self.text)
        tokens = word_tokenize(tokens)
        clean_text = []
        stoplist = set(stopwords.words('english') + list(punctuation))

        for token in tokens:
            l_token = token.lower()
            if l_token not in stoplist:
                clean_text.append(l_token)

        return clean_text

    def _text_to_frequency_token_words(self):
        clean_text = self._text_to_token_words()
        frequency = FreqDist(clean_text)
        max_frequency = max(frequency.values())
        for word in frequency.keys():
            frequency[word] = frequency[word] / max_frequency

        return frequency

    def _sentence_scores_analyze(self, frequency):
        sentences = sent_tokenize(self.text)
        sentence_scores = dict()
        for sentence in sentences:
            if len(sentence.split(' ')) < 26:
                for word in word_tokenize(sentence.lower()):
                    if word in frequency.keys():
                        if sentence not in sentence_scores.keys():
                            sentence_scores[sentence] = frequency[word]
                        else:
                            sentence_scores[sentence] += frequency[word]
        return sentence_scores

    def _summarize(self):
        frequency_tokens = self._text_to_frequency_token_words()
        sentence_scores = self._sentence_scores_analyze(frequency_tokens)
        summary_sentences = heapq.nlargest(4, sentence_scores, key=sentence_scores.get)
        x = [word for word in summary_sentences]
        self.summary = ''.join(x)

    def _article_text(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)

        if not driver.find_elements_by_xpath("//h1[@class='ssrcss-gcq6xq-StyledHeading e1fj1fc10']"):
            self.text += driver.find_elements_by_xpath("//div[@class='article__body-content' or @class='qa-story-body story-body gel-pica gel-10/12@m gel-7/8@l gs-u-ml0@l gs-u-pb++']")[0].get_attribute(
                "textContent")
        else:
            self.text += driver.find_elements_by_xpath("//h1[@class='ssrcss-gcq6xq-StyledHeading e1fj1fc10']")[0].text
            text_sentence = driver.find_elements_by_xpath("//p[@class='ssrcss-1q0x1qg-Paragraph eq5iqo00']")
            for par in text_sentence:
                self.text += '\n' + par.get_attribute("textContent")

    def article_process(self):
        self._article_text()
        self._summarize()
        self._calc_sentiment()
