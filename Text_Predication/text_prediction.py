import pandas as pd
from nltk import bigrams
from nltk.lm.preprocessing import pad_both_ends
from nltk.tokenize import WordPunctTokenizer
from nltk.lm import Vocabulary
from nltk.lm import Laplace


def remove_html_tags(text):
    # Function to remove HTML tags from text
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def remap_corpus(path):
    # Read CSV file, preprocess the 'Body' column, and tokenize the text
    df_corpus = pd.read_csv(path)
    df_corpus['Body'] = df_corpus['Body'].apply(lambda x: remove_html_tags(x))
    df_corpus['Body_tokenized'] = df_corpus['Body'].apply(lambda x: WordPunctTokenizer().tokenize(x))
    return df_corpus


def padding_corpus(corpus):
    # Pad both ends of each sentence in the corpus
    corpus_padding = []
    for sentence in corpus:
        corpus_padding.append(
            list(pad_both_ends(sentence, pad_left=True, left_pad_symbol="<s>", pad_right=True, right_pad_symbol="</s>",
                               n=2)))
    return corpus_padding


def remap_bigram(corpus):
    # Extract bigrams from each sentence in the corpus
    corpus_bigram = []
    for sentence in corpus:
        corpus_bigram.append(list(bigrams(sentence)))
    return corpus_bigram


def vocab(corpus):
    # Create a vocabulary list from the corpus
    voc_list = []
    for sentence in corpus:
        for word in sentence:
            voc_list.append(word)
    return Vocabulary(voc_list, unk_cutoff=3)


def prediction(train, prefix):
    # Perform next-word prediction using Laplace smoothing
    train = padding_corpus(train)
    voc = vocab(train)
    LaplaceModel = Laplace(2, vocabulary=voc)
    train = remap_bigram(train)
    LaplaceModel.fit(train)
    score_list = {}
    for word in voc:
        score_list[word] = LaplaceModel.score(word, [prefix])
    sorted_dict = dict(sorted(score_list.items(), key=lambda item: item[1], reverse=True))
    my_dict = {k: round(sorted_dict[k], 2) for k in list(sorted_dict.keys())[:3]}
    return my_dict


if __name__ == '__main__':
    # Main execution
    print("Text Prediction using Laplace Smoothing")
    print("--------------------------------------")
    print("Reading training data...")

    path_train = "corpus/train.csv"
    corpus_train = remap_corpus(path_train)['Body_tokenized']
    print("Training data is ready!")
    print("--------------------------------------")
    user_input = input("Enter a prefix for next-word prediction: ")
    print("--------------------------------------")
    print("Performing next-word prediction...")

    prediction_result = prediction(corpus_train, user_input)
    print("------- Result of Prediction ---------")
    for i in prediction_result:
        print(f"Next word predictionc can be : {i}")
