import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import re
import itertools
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory



class Preprocessing:
    def __init__(self,dataframe):
        typo = dataframe
        self.normal_dict = dict(zip(typo["false"], typo["true"]))

    def __repr__(self):
        return f"Preprocessing proses for sentimen analysis"

    def remove_newline(self):
        return re.sub('\n', ' ', self.data)

    def remove_username(self):
        text = re.sub(r'@[A-Za-z0-9_]+', '', self.data)
        return text

    def remove_url(self):
        return re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', ' ', self.data)

    def remove_non_alphabet(self):
        output = re.sub('[^a-zA-Z ]+', ' ', self.data)
        return output

    def remove_excessive_whitespace(self):
        return re.sub('  +', ' ', self.data)

    def repeating_char(self):
        return ''.join(''.join(s)[:2] for _, s in itertools.groupby(self.data))

    def spelling_correction(self):
        word_list = self.data.split()
        word_list_len = len(word_list)
        transformed_word_list = []
        i = 0
        while i < word_list_len:
            if (i + 1) < word_list_len:
                two_words = ' '.join(word_list[i:i + 2])
                if two_words in self.normal_dict:
                    transformed_word_list.append(self.normal_dict[two_words])
                    i += 2
                    continue
            transformed_word_list.append(self.normal_dict.get(word_list[i], word_list[i]))
            i += 1
        return ' '.join(transformed_word_list)

    def stemming(self):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        output = stemmer.stem(self.data)
        return output

    def stopword_removal(self):
        konjungsi = ["ya", "tidak"]
        stopword = [line.strip('\n') for line in open('flaskr/stopword.txt')]
        word_list = self.data.split()
        text = []
        for i in word_list:
            if i not in stopword:
                if i in konjungsi:
                    text.append(i)
                else:
                    if len(i) > 2:
                        text.append(i)
        return ' '.join(text)

    def preprocessing(self,data):
        self.data = str(data)
        self.data = self.data.lower()
        self.data = self.remove_newline()
        self.data = self.remove_username()
        self.data = self.remove_url()
        self.data = self.remove_non_alphabet()
        self.data = self.remove_excessive_whitespace()
        self.data = self.repeating_char()
        self.data = self.spelling_correction()
        self.data = self.stopword_removal()
        self.data = self.stemming()
        return self.data
