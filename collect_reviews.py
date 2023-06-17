from deepface import DeepFace
from util import get_soup, argmax, append_to_json
import traceback
import mysql.connector
import datetime
import argparse


MAX_RESTAURANTS = 20
MIN_ASIANS = 10

parser = argparse.ArgumentParser()
parser.add_argument('--zip_code', type=int, required=True)
args = parser.parse_args()
attributes = vars(args)
zip_code = attributes['zip_code']


print("start!\n")

#zip_code = int(input("Enter desired zip code: "))
#zip_code = 14618

# Get restaurants given area
area_url = f'https://www.yelp.com/search?find_desc=Chinese+Food&find_loc={zip_code}'
area_soup = get_soup(area_url)
# This could be better
restaurant_ids = area_soup.select("a[href*='biz']")
restaurant_ids = list(map(lambda x: x['href'], restaurant_ids))[:MAX_RESTAURANTS]

mydb = mysql.connector.connect(
  host="db",
  user="root",
  password="root",
  database="asian_yelp"
)
mycursor = mydb.cursor()
date = datetime.date.today()
table_name = f'reviews_{zip_code}'
mycursor.execute(
    f"CREATE TABLE IF NOT EXISTS {table_name} "
    f"(restaurant_id VARCHAR(255), "
    f"user_id VARCHAR(255), "
    f"guessed_race VARCHAR(255), "
    f"star_rating INT, "
    f"comment LONGTEXT)"
)

# For each restaurant, get reviews
for restaurant_id in restaurant_ids:

    count_asians = 0
    page_count = 0

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
                    print(f'error!')
                    #print(traceback.format_exc())

                sql = f"INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s)"
                val = (restaurant_id, user_id,  guessed_race, star_rating, comment)
                mycursor.execute(sql, val)

                results_url = f'results_{zip_code}.json'
                result = {
                    'restaurant_id': restaurant_id,
                    'user_id': user_id,
                    'guessed_race': guessed_race,
                    'star_rating': star_rating,
                    'comment': comment
                }
                append_to_json(results_url, result)

            except Exception as e:
                print(e)
                print(traceback.format_exc())
                pass

        mydb.commit()
        page_count += 1

print("\ndone!")
