import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="asian_yelp"
)

mycursor = mydb.cursor()

zip_code = 14618
#  TODO: DATE
table_name = f'reviews_{zip_code}'

result = {
  'restaurant_id': 'a',
  'user_id': 'a',
  'guessed_race': 'a',
  'star_rating': 4,
  'comment': 'a'
}

sql = f"INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s)"
val = ('a','b','c','3','d')
mycursor.execute(sql, val)

mydb.commit()
