FROM python:3.8
ADD twitter_keyword.py .
ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "./twitter_keyword.py"]