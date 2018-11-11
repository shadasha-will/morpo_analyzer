import os
import json
import math
from collections import Counter

import spacy
from nltk.corpus import stopwords

from word_embedding import word2vec_model
import config

nlp = spacy.load('es')

""" script for creating a minimally supervised morphological analyzer as described by Yarowsky and Wincentowski """




class MorphoAnalyser:

    """ class with all features for creating an instance of a morphological analyser"""
    def __init__(self, infectional_table_path, corpus):
        # load the table of infectional parts of speech as a json object
        with open(infectional_table_path) as infectional_table_json:
            self.inflections = json.loads(infectional_table_json.read())
        # load another corpus for loading the neccesary terms
        self.corpus = corpus
        self.stop_words = stopwords.words("spanish")
        self.word_frequency = {}
        self.word2vec_model = word2vec_model(config.training_corpus)

    def get_inflection_root_ratios(self, root, term):
        """
        function align the similarites of two words based on their frequencies
        :param root: possible root for a given word
        :param term: possible inflected given term
        :return:
        """
        inf_root_ratio = math.log(self.word_frequency[term] / self.word_frequency[root])
        return inf_root_ratio

    def get_frequency(self, training_corpus_path):
        """
        function to get the frequency of words in the training corpus
        :param training_corpus_path: path to training corpus
        :return: null
        """
        with open(training_corpus_path, 'r') as t_corpus:
            words = t_corpus.read().split()
            word_freqs = Counter(words)
            self.word_frequency = word_freqs

    @staticmethod
    def get_candidates(tag, input_doc):
        """
        funtion to get all candidate tokens of a certain pos type
        :param tag: part of speech tag of interest
        :param input_doc: spacy input document
        :return: list of candidate strings of a certain type
        """
        tag_candidates = []
        for word in input_doc:
            word_tag = word.tag_.split('__')[0]
            if tag == word_tag:
                tag_candidates.append(word.text)
        return tag_candidates

    def get_context_similarity(self, term1, term2):
        """
        function to get the context similarity of two terms in the corpus
        from the word2vec model
        :param term1: first term
        :param term2: second term
        :return: the context similarity
        """
        similarity = self.word2vec_model.similarity(term1, term2)
        return similarity


    def load_terms(self, path_to_corpus):
        """
        method to load a corpus and extract a candidate list of noun verb and adjective roots
        :param path_to_corpus: path to a corpus in
        :return: null
        """

        candidate_adj = []
        candidate_verbs = []
        candidate_nouns = []

        print("Loading the file {} for candidate word form processing".format(path_to_corpus))

        with open(path_to_corpus, "r") as input_corpus:
            words = input_corpus.read().split()
            for i in range(0, len(words), 1000):
                current_chunk = words[i:i + 1000]
                spacy_text = nlp(' '.join(current_chunk))
                candidate_adj.extend(self.get_candidates('ADJ', spacy_text.doc))
                candidate_nouns.extend(self.get_candidates('NOUN', spacy_text.doc))
                candidate_verbs.extend(self.get_candidates('VERB', spacy_text.doc))

        # start writing the candidate terms to aidfferent files (line separated lists)
        with open(path_to_corpus + '_nouns', "w") as out_noun_list:
            candidate_nouns = set(candidate_nouns)
            for noun in candidate_nouns:
                out_noun_list.write('{} \n'.format(noun))

        with open(path_to_corpus + '_adj', "w") as out_adj_list:
            candidate_adj = set(candidate_adj)
            for adj in candidate_adj:
                out_adj_list.write('{} \n'.format(adj))

        with open(path_to_corpus + "_verbs", "w") as out_verb_list:
            candidate_verbs = set(candidate_verbs)
            for term in candidate_verbs:
                out_verb_list.write('{} \n'.format(term))

        print("Finished processing the candidate forms")

if __name__ == '__main__':
    analyzer = MorphoAnalyser(config.inflection_file, config.corpus_data)
    # check to see if we have loaded the test corpus for extracting candidate nouns
    if not os.path.exists(config.corpus_data + '_nouns'):
        analyzer.load_terms(analyzer.corpus)
    analyzer.get_context_similarity('hacen', 'haciendo')

