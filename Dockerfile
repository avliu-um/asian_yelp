# syntax=docker/dockerfile:1
FROM python
WORKDIR code/ 
RUN pip3 install --upgrade pip
#RUN git clone https://github.com/avliu-um/asian_yelp.git
# https://superuser.com/questions/164553/automatically-answer-yes-when-using-apt-get-install
# Source: https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo
RUN apt-get --yes update && apt-get --yes install libgl1

COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

COPY collect_reviews.py collect_reviews.py
COPY util.py util.py
COPY run.sh run.sh

ENTRYPOINT ["sh", "./run.sh"]
