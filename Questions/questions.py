import nltk
import sys
import os
import string
import math

nltk.download('stopwords')

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
    dict = {}  # Initalize the dicctionary

    # Getting the directory path and the filenames
    for (dirpath, dirnames, filenames) in os.walk(directory):
        contents = []

        # Store all the file's contents as a string in list called contents
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            with open(file_path) as f:
                contents.append(str(f.read()))

    # Fill the dictionary with the filename as a key and the file's content as a value
    for i in range(len(filenames)):
        dict[filenames[i]] = contents[i]

    return dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.    """

    punctuations = set(string.punctuation)

    word_tokenized = nltk.word_tokenize(document)

    word_list_output = []

    for word in word_tokenized:
        word = str(word).lower()
        if word in punctuations or word in nltk.corpus.stopwords.words(
                "english"):  # Filter out all english stop words and punctuations
            continue
        else:
            word_list_output.append(word)

    return word_list_output


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
     # Create a set that should contain all words in documents that that appear at least in one of the documents
    words = set() 

    # Get all words in documents that appear at least in one of the documents

    for key in documents:
        words.update(documents[key])

    idfs = dict()

    # Computing the inverse document frequency

    for word in words:
        f = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    if n > len(files):
        raise Exception("Sorry, the entered number is greater than the total number of files.")

    for filename in files:

        # Count frequencies

        frequencies = dict()

        for word in files[filename]:
            if word not in frequencies:
                frequencies[word] = 1
            else:
                frequencies[word] += 1

        files[filename] = frequencies

    # Calculate TF-IDFs
    tfidfs = dict()

    for filename in files:
        tfidfs[filename] = []
        for word in files[filename]:
            tf = files[filename][word]
            if word in query:
                tfidfs[filename].append(tf * idfs[word])

    filename_list = []
    filename_value = []

    for filename in tfidfs:
        filename_value.append(sum(tfidfs[filename]))
        filename_list.append(filename)

    # Rank the files ranked according to the sum of tf-idf values

    filename_value, filename_list = zip(*sorted(zip(filename_value, filename_list), reverse=True))

    return list(filename_list[:n])


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    if n < len(sentences):
        # Sentences_idfs_density is a dictionary that mapping each sentence to its sum of IDF values for each word in the sentence 
        # and to its query term density
        sentences_idfs_density = dict() 

        for sentence in sentences:  # Iterate over all sentence in the dictionary
            sum_sentence_idfs = 0
            sum_density = 0
            for word in query:
                if word in sentences[sentence]:
                    sum_sentence_idfs += idfs.get(word)
                    sum_density += 1
            query_term_density = sum_density / len(sentence)
            sentences_idfs_density[sentence] = (sum_sentence_idfs, query_term_density)

        # Sort sentences_idfs_density by the idf value of each word (first) and its query term density (second)
        top_sentence = sorted(sentences_idfs_density,
                              key=lambda k: (sentences_idfs_density[k][0], sentences_idfs_density[k][1]), reverse=True)

        return top_sentence[:n]

    else:
        raise Exception("n is greater than the total number of sentences.")


if __name__ == "__main__":
    main()
