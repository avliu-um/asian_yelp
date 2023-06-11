# Asian Yelp

This is a project to lift minority voices in majority-white environments.

As an Asian foodie, I'm always on the hunt for the best Asian restaurants around town. 
However, as somebody who lives in a majority-white environment, review sites such as Yelp tend to have ratings and reviews hidden behind a white Majority.
A star rating of 4 in my area, for instance, generally means that whites on average thought it was a 4.

This project filters Yelp reviews to those from Asian reviewers in an effort to uplift their minority voice.
It allows those with roots and connections to Asian cuisine, culture, experience, and knowledge, to speak at the forefront.

The main goal of this project is this: For a given area, find "hidden gems" of restaurants, i.e. those whose star ratings dramatically increase as a result of filtering on Asian reviewers.

Included files:
- collect_reviews.py - for a given zip code, collects 10 reviews each of 20 restaurants, filtered by Asians using the [DeepFace](https://github.com/serengil/deepface) package, and writes to a mysql server
- requirements.txt - required packages
