# syntax=docker/dockerfile:1
FROM python
WORKDIR code/ 
COPY . . 
RUN pip3 install --upgrade pip
RUN git clone https://github.com/avliu-um/asian_yelp.git
# https://superuser.com/questions/164553/automatically-answer-yes-when-using-apt-get-install
# Source: https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo
RUN apt-get --yes update && apt-get --yes install libgl1
RUN pip install -r asian_yelp/requirements.txt
CMD ["python", "./asian_yelp/collect_reviews.py"]
