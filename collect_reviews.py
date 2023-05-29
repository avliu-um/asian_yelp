import numpy as np

from deepface import DeepFace

from util import get_soup, append_to_json, argmax
import traceback


MAX_RESTAURANTS = 20
MIN_ASIANS = 10


zip = int(input("Enter desired zip code: "))

# Get restaurants given area
area_url = f'https://www.yelp.com/search?find_desc=Chinese+Food&find_loc={zip}'
area_soup = get_soup(area_url)
# This could be better
restaurant_ids = area_soup.select("a[href*='biz']")
restaurant_ids = list(map(lambda x: x['href'], restaurant_ids))[:MAX_RESTAURANTS]

results = []
count_asians = 0
page_count = 0

# For each restaurant, get reviews
for restaurant_id in restaurant_ids:

    while count_asians < MIN_ASIANS:

        restaurant_url = f'https://yelp.com{restaurant_id}&start={page_count*10}&sort_by=date_desc#reviews'
        restaurant_soup = get_soup(restaurant_url)
        reviews = restaurant_soup.select("li[class*='margin']")

        for review in reviews:
            try:
                # Get user photo url
                user_extension = review.select_one("a[href^='/user_details']")['href']
                user_id = user_extension[user_extension.find('userid=') + len('userid='):]
                # testing
                # user_id = 'pMwX3DV1s7rP3AaoH0HIFQ'
                user_url = f'https://www.yelp.com/user_details?userid={user_id}'

                print('looking at user id {0}'.format(user_id))

                # Get review star rating
                star_rating = int(
                    review.select_one("div[class*='five-stars']")['aria-label'][0]
                )

                comment = review.select_one("p[class*='comment']").text

                # Get user photo
                user_soup = get_soup(user_url)
                user_photo_url = user_soup.select_one('div.user-profile_avatar img')['src']

                # Guess user race
                guessed_race = None
                try:
                    guessed_race_dict = DeepFace.analyze(
                        img_path=user_photo_url,
                        actions=['race']
                    )
                    guessed_race = argmax(guessed_race_dict[0]['race'])
                    if guessed_race and guessed_race == "asian":
                        count_asians += 1
                    print(f'user is predicted {guessed_race}')
                except ValueError as e:
                    print(traceback.format_exc())

                result = {
                    'restaurant_id': restaurant_id,
                    'user_id': user_id,
                    'guessed_race': guessed_race,
                    'star_rating': star_rating,
                    'comment':  comment
                }
                results_url = f'results_{zip}.json'
                append_to_json(results_url, result)

            except Exception as e:
                print(e)
                print(traceback.format_exc())
                pass

        page_count += 1
