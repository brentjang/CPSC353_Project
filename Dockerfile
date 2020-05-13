FROM python:3

COPY . usr/src/cpsc353_project/

WORKDIR usr/src/cpsc353_project/

RUN pip install -r requirements.txt

CMD [ "python3", "./clone_repo.py", "./got3_pull.py", "./twitter_sentiment.py"]