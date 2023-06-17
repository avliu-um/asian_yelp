# Asian Yelp

This is a project to lift minority voices in majority-white environments. From a technical standpoint, it is a fully-containerized web-scraping project of the Yelp platform.

## Motivation and Description

As an Asian foodie, I'm always on the hunt for the best Asian restaurants around town. 
However, as somebody who lives in a majority-white environment, review sites such as Yelp tend to have ratings and reviews hidden behind a white Majority.
A star rating of 4 in my area, for instance, generally means that whites on average thought it was a 4.

This project filters Yelp reviews to those from Asian reviewers in an effort to uplift their minority voice.
It allows those with roots and connections to Asian cuisine, culture, experience, and knowledge, to speak at the forefront.

The main goal of this project is this: For a given area, find "hidden gems" of restaurants, i.e. those whose star ratings dramatically increase as a result of filtering on Asian reviewers. Right now, it just runs through 20 Chinese restaurants in a given zip code, scrapes reviews until at least 10 Asians are encountered, and writes in two places: (1) a MySQL DB and (2) a json folder.

## Usage

This project is fully containerized using Docker. The scraper is run on a Python-based container with requirements installed, and writes data to a MySQL container using the MySQL-connector [package](https://dev.mysql.com/doc/connector-python/en/). 

Execute the following to run the scraper on the desired zip code (ZIP_CODE):
```
1. docker-compose up
2. docker-compose run scraper [ZIP_CODE]
```

After running, the data is contained in the "asian_yelp" database in the "db" container.

## Included files
- collect_reviews.py - for a given zip code, collects 10 reviews each of 20 restaurants, filtered by Asians using the [DeepFace](https://github.com/serengil/deepface) package, and writes to a mysql server
- requirements.txt - required packages
- Dockerfile - Docker build file for the scraper
- docker-compose.yml - Docker compose file for the scraper and associated database
