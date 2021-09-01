FROM python:3
ADD test_text.txt /
RUN pip install ipclassifier
RUN python -m nltk.downloader words cmudict averaged_perceptron_tagger wordnet
