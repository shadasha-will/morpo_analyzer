""" config file for the morphological analyzer project """

import os

#data_directory = "/data"

data_directory = "tests"

# path for the inflections of verbs in Spanish
inflection_file = os.path.join(data_directory, 'spanish_inflections.json')

# loading the
#training_corpus = os.path.join(data_directory, "split_corpus_1")
contest_sim_corpus = os.path.join(data_directory, "split_corpus_2")

corpus_data = 'test_corpus'

training_corpus = os.path.join(data_directory, 'test_training_corpus')