# полный путь к исходному файлу с данными по твиттам
FILEPATH = '\\three_minutes_tweets.json.txt'

# полный путь к файлу с калькуляцией эмоциональной окраски
FILEPATH_AF = '\\AFINN-111.txt'

# имя БД
db = '\\mts_twits.db'

log_conf = '\\logger_config.conf'

logpath = '\\twitter_info_project.log'

sql = ("""CREATE TABLE IF NOT EXISTS users (
user_id int NOT NULL PRIMARY KEY, 
username text, 
url text, 
location text,
lang text
);""",
       """CREATE TABLE IF NOT EXISTS twitts (
tweet_id int NOT NULL PRIMARY KEY, 
created_at text,
user_id int,
tweet_text text, 
country_code text, 
sentiment int
);""")
