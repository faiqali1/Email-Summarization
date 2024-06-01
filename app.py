

from sumy.utils import get_stop_words
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

import re

import streamlit as st
# import nltk
# nltk.download('punkt')


def extract_salutation(text):
    """
    Extracts the salutation line from the given text.
    """
    salutation_pattern = r'^(Hi|Hello|Dear|Greetings|Regards|Hi there|Hey|Good [mM]orning|Good [aA]fternoon|Good [eE]vening),?[\s\r\n]'
    match = re.search(salutation_pattern, text, re.MULTILINE)
    if match:
        return match.group(0).strip(',')
    return ''


def extract_signature(text):
    """
    Extracts the signature block from the given text.
    """
    signature_pattern = r'(?:\n\r?(?:--\r?\n|__\r?\n)|[-\*\s][-\*\s]+\r?\n)(\r?\n\r?[-\w\s,\.@]+(?:\r?\n[-\w\s,\.@]+)*)'
    match = re.search(signature_pattern, text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ''


def preprocess_text(text):
    """
    Performs text preprocessing steps on the given text using spaCy.
    """
    salutation = extract_salutation(text)
    text = text.replace(salutation, '', 1) if salutation else text

    signature = extract_signature(text)
    text = text.replace(signature, '')

    return text


def summarizing(message):
    LANGUAGE = "english"
    SENTENCES_COUNT = 3

    if __name__ == "__main__":
        # for plain text files there exists two possibilities as following
        # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
        parser = PlaintextParser.from_string(message, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        string = ''

        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            # print(sentence)
            string += str(sentence) + '\n'

        return string


def main():
    st.title("Email Summarizer")
    email_text = st.text_area("Enter the email text:")

    if st.button("Summarize"):
        if email_text:
            text = preprocess_text(email_text)
            summary = summarizing(text)
            st.subheader("Summary")
            st.write(summary)
        else:
            st.warning("Please enter some text to summarize.")


if __name__ == "__main__":
    main()
