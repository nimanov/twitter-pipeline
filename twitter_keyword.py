import time
import datetime
import psycopg2
import psycopg2.extras
from psycopg2 import errors
from datetime import date, timedelta
import snscrape.modules.twitter as snstwitter
from psycopg2.errorcodes import UNIQUE_VIOLATION


def write_to_database(url_tweet, date_tweet, raw_content, p_username, user_displayname, user_profile_url, keyword):
    # DATABASE INFO
    hostname = '172.18.0.2'
    database = 'neurotime'
    pwd = 1234
    username = 'nurlan'
    port_id = 5432
    conn = None
    scraped_date = str(datetime.datetime.now())
    try:
        with psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                create_script = ''' CREATE TABLE IF NOT EXISTS twitter(
                                        id               BIGSERIAL NOT NULL PRIMARY KEY,
                                        url_tweet        VARCHAR UNIQUE,
                                        date_tweet       VARCHAR,
                                        raw_content      VARCHAR,
                                        username         VARCHAR,
                                        user_displayname VARCHAR,
                                        user_profile_url VARCHAR,
                                        keyword          VARCHAR,
                                        scraped_date     VARCHAR)
                                        '''
                cur.execute(create_script)
                insert_script = '''INSERT INTO twitter 
                                    (url_tweet, date_tweet, raw_content, username, user_displayname, 
                                    user_profile_url, keyword, scraped_date) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                 '''
                record = (url_tweet, date_tweet, raw_content,
                          p_username, user_displayname, user_profile_url, keyword, scraped_date,)
                cur.execute(insert_script, record)
                print("Written to database", str(datetime.datetime.now()), keyword, url_tweet, flush=True)
    except errors.lookup(UNIQUE_VIOLATION):  # Means this url already scraped
        #print("Already in", url_tweet, flush=True)
        return "continue"
    except Exception as error:
        f_error_log = open("error.log", "a", encoding="utf-8")
        msg = "DATABASE ERROR " + str(datetime.datetime.now()) + " "
        f_error_log.write(msg + " ==> " + str(error) + "\n")
        f_error_log.close()
        return -1
    finally:
        if conn is not None:
            conn.close()
    return 1


def twitter_scraper(keywords: list):
    yesterday = str(date.today() - timedelta(1))
    tomorrow = str(date.today() + timedelta(1))  # Since the 'until:' part is excluded
    for keyword in keywords:
        query = keyword + " until:" + tomorrow + " since:" + yesterday
        for tweet in snstwitter.TwitterSearchScraper(query).get_items():
            url_tweet = vars(tweet)['url'].strip()
            date_tweet = vars(tweet)['date']
            raw_content = vars(tweet)['rawContent']
            p_username = vars(tweet)['user'].username
            user_displayname = vars(tweet)['user'].displayname
            user_profile_url = str(vars(tweet)['user'])
            return_value = write_to_database(url_tweet, date_tweet, raw_content, p_username,
                                             user_displayname, user_profile_url, keyword)
            if return_value == "continue":  # Means this url already scraped
                continue
            if return_value == -1:
                return "DATABASE ERROR"


while True:
    twitter_scraper(["təhsil", "iqtisadiyyat"])
    print("Finished the cycle", str(datetime.datetime.now()), flush=True)
    time.sleep(3600)
