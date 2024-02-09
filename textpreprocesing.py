import re
import string
import pandas as pd
from tqdm import tqdm
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class DataPreprocessing:
    def __init__(self, dataframe):
        # You can initialize any parameters or configurations here
        self.dataframe = dataframe
        self.kamus_normalisasi = pd.read_csv("slang.csv")  # Assuming 'slang.csv' contains slang and normalized words

    def filtering_text(self, text):
        # Implementation of filtering_text function
        text = text.lower()
        text = re.sub(r'https?:\/\/\S+', '', text)
        text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", text).split())
        text = re.sub(r'(b\'{1,2})', "", text)
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def stop_stem(self, text):
        # Implementation of stop_stem function
        with open('kamus.txt') as kamus:
            word = kamus.readlines()
            list_stopword = [line.replace('\n', "") for line in word]
        dictionary = ArrayDictionary(list_stopword)
        stopword = StopWordRemover(dictionary)
        text = stopword.remove(text)
        factory_stemmer = StemmerFactory()
        stemmer = factory_stemmer.create_stemmer()
        text = stemmer.stem(text)
        return text

    def normalize_slang(self, text):
        # Implementation of normalize_slang function
        for _, row in self.kamus_normalisasi.iterrows():
            slang_word = row['slang']
            normalized_word = row['formal']
            text = re.sub(r'\b' + slang_word + r'\b', normalized_word, text)
        return text

    def text_preprocessing(self, input_column, output_column):
        tqdm.pandas()  # Use tqdm's progress_apply instead of apply
        self.dataframe[output_column] = self.dataframe[input_column].progress_apply(self.filtering_text)
        self.dataframe[output_column] = self.dataframe[output_column].progress_apply(self.stop_stem)
        self.dataframe[output_column] = self.dataframe[output_column].progress_apply(self.normalize_slang)

# Example usage:
# Assuming you have a DataFrame named 'data_tweet' with a column 'text'
# data_tweet = pd.DataFrame({'text': ["Your raw text here", "Another text with slang"]})
# data_preprocessor = DataPreprocessing(data_tweet)
# data_preprocessor.text_preprocessing('text', 'clean_text')
# print(data_tweet)
