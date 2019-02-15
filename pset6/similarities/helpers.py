from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # TODO
    # creates a set of lines for both files
    linesA = set(a.splitlines())
    linesB = set(b.splitlines())

    # returns the common lines from both sets
    return linesA & linesB


def sentences(a, b):
    """Return sentences in both a and b"""

    # TODO
    # creates a set of sentences for both files
    sentencesA = set(sent_tokenize(a))
    sentencesB = set(sent_tokenize(b))

    # returns the common sentences from both sets
    return sentencesA & sentencesB


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # TODO
    # creates two empty lists
    c = []
    d = []

    # iterates over both lists and appends substrings of length n
    for i in range(len(a) - n + 1):
        c.append(a[i:i + n])
    for i in range(len(a) - n + 1):
        d.append(b[i:i + n])

    # converts lists to sets to return common substringds
    substringA = set(c)
    substringB = set(d)

    # returns the common substrings of length n from both sets
    return substringA & substringB
