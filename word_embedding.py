import re

from gensim.models import Word2Vec

""" function to get word embeddings for word similarity"""

def word2vec_model(training_corpus_path):
    """
    function to create word vectors from a training corpus
    :param training_corpus_path: path to a training corpus with sentences separated by lines
    :return: word2vec model
    """
    with open(training_corpus_path, 'r') as train_corpus:
        sentences = train_corpus.read().split('\n')
        # get lemmatized sentences
        for sent in range(len(sentences)):
            # split sentences in to words and remove
            punct_removed = re.sub('[^\w]', '', sentences[sent])
            sentences[sent] = punct_removed.split()[:-1]
        print("Training the Word2Vec model")
        model = Word2Vec(sentences)
        model_path = 'model.bin'
        print("Saving the model to the path {}".format(model_path))
        return model