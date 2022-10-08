import nltk
import os, sys
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    file_str = {}
    dirs = os.listdir(directory)

    for file_name in dirs:
        with open(os.path.join(directory, file_name), encoding='utf-8') as file:
            file_str[file_name] = file.read()
    
    return file_str


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    right_word_list = []

    word_list = nltk.word_tokenize(document)

    for word in word_list:
        if not (word in string.punctuation and word in nltk.corpus.stopwords.words("english")):
            right_word_list.append(word)
    
    return right_word_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    word_dict = {}

    for doc in documents:
        for word in documents[doc]:
            if word not in word_dict:
                word_dict[word] = []
                word_dict[word].append(doc)
            elif doc not in word_dict[word]:
                word_dict[word].append(doc)
    
    result_dic = {}

    total_num_doc = len(documents)

    for word, docs in word_dict.items():
        result_dic[word] = math.log(total_num_doc / len(docs))
    
    return result_dic


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_score = {}
    for file in files:
        file_score[file] = 0
    
    for word in query:
        for file, word_list in files.items():
            tf = word_list.count(word)
            file_score[file] += tf * idfs[word]
    
    rank_desc = sorted(file_score.items(), key=lambda item: item[1], reverse=True)

    return [file[0] for file in rank_desc[:n]]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_dict = {}
    
    for sentence in sentences:
        sentence_dict[sentence] = [0, 0]
    
    for word in query:
        for sentence, word_list in sentences.items():
            if word in word_list:
                sentence_dict[sentence][0] += idfs[word]
                sentence_dict[sentence][1] += word_list.count(word) / len(word_list)

    rank = sorted(sentence_dict.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)

    return [sentence[0] for sentence in rank[:n]]


if __name__ == "__main__":
    main()
