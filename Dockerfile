FROM python:3
ADD test_text.txt /
RUN pip install ipclassifier
