from gensim.utils import simple_preprocess
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
import spacy
from typing import List
from time import time
import pandas
from rich.progress import track


def sent_to_words(biographies_column: pandas.core.series.Series) -> list:
    t = time()
    biographies_column = biographies_column.astype('str')
    tokenizer = RegexpTokenizer(r'\w+')
    biographies_tokenized = list(biographies_column.apply(tokenizer.tokenize).values)
    print('Time to tokenize everything: {} mins'.format(round((time() - t) / 60, 2)))
    return biographies_tokenized


def lemmatization(tokenized_biographies: list, allowed_postags=['NOUN', 'VERB']) -> list:
    texts_out = []
    for sent in track(tokenized_biographies, description="lemmatize biographies"):
        nlp = spacy.load('fr_core_news_sm')
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def remove_stopwords(tokenized_biographies: list, stop_words) -> list:
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in
            track(tokenized_biographies, description="removing stop words")]


def remove_stop_words_from_biographies(
        biographies_column: pandas.core.series.Series,
        custom_stop_words: List[str] = None,
        use_lemmatization=False,
        allowed_postags=['NOUN', 'VERB']) -> list:
    tokenized_biographies: list = sent_to_words(biographies_column=biographies_column)
    stop_words = stopwords.words('french')
    if custom_stop_words:
        stop_words.extend(custom_stop_words)
    if use_lemmatization:
        tokenized_biographies = lemmatization(tokenized_biographies, allowed_postags=allowed_postags)
    return remove_stopwords(tokenized_biographies=tokenized_biographies, stop_words=stop_words)
