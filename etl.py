from yelpapi import YelpAPI
import wikipedia
import mysql.connector
from datetime import datetime

def sql_insert(sql_call, data):

    mydb = mysql.connector.connect(
      host="host",
      user="user",
      passwd="password",
      database="database"
    )

    mycursor = mydb.cursor()
    mycursor.execute(sql_call, data)
    mydb.commit()

def sql_get_id(table, key, value):
    mydb = mysql.connector.connect(
      host="host",
      user="user",
      passwd="password",
      database="database"
    )

    cursor = mydb.cursor()

    sql_select = "SELECT * FROM `{}` WHERE `{}`='{}' LIMIT 1".format(table,key,value)
    cursor.execute(sql_select)
    data = cursor.fetchone()
    if data is None:
        return None
    else:
        return data[0]

def check_parking(business):
    for d in business['categories']:
        if d['alias'] == 'parking':
            return True
    return False

def get_wikipedia_url(name):
    try:
       page = wikipedia.page(name)
       if page.title != name:
           url = None
       else:
           url = page.url
    except:
       url = None
    return url

def get_user_reviews(business_id):
    api_key = 'api_key'
    yelp_api = YelpAPI(api_key, timeout_s=3.0)
    reviews = yelp_api.reviews_query(id=business_id)
    review_list = reviews['reviews']
    most_recent_review = max(review_list, key=lambda x:datetime.strptime(x['time_created'], '%Y-%m-%d %H:%M:%S'))
    user_id = most_recent_review['user']['id']
    user_profile = most_recent_review['user']['profile_url']
    return (user_id, user_profile)

def update_location_table(location_name):
    # take existing id or create
    id = sql_get_id('locations','location',location_name)
    if id is None:
        data = (location_name, )
        sql_call = "INSERT INTO locations (location) VALUES (%s)"
        sql_insert(sql_call, data)
        id = sql_get_id('locations','location',location_name)
    return id

def update_user_table(user_data):
    # take existing id or create
    yelp_id = user_data[0]
    user_url = user_data[1]
    id = sql_get_id('users','yelp_user_id',yelp_id)
    if id is None:
        sql_call = "INSERT INTO users (yelp_user_id, user_url) VALUES (%s, %s)"
        sql_insert(sql_call, user_data)
        id = sql_get_id('users','yelp_user_id',yelp_id)
    return id

def update_business_db(business_data,location_data,user_data):
    loc_id = update_location_table(location_data)
    user_id = update_user_table(user_data)
    business_data = business_data + (loc_id, user_id,)
    sql_call = "INSERT INTO businesses(name, rating, wiki_url, parking, open_weekends, location_id, most_recent_review_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    sql_insert(sql_call, business_data)

def open_weekends(business_id):
    api_key = 'api_key'
    yelp_api = YelpAPI(api_key, timeout_s=3.0)
    business_result = yelp_api.business_query(id=business_id)
    hours = business_result.get('hours',[{'open':[{},{}]}])
    hours = hours[0]['open']
    open_sat = False
    open_sun = False
    for d in hours:
        if d.get('day',9)==5:
            open_sat = True
            continue
        if d.get('day',9)==6:
            open_sun= True
            continue
    if not open_sat or not open_sun:
        return False
    return True

def get_businesses(offset):
    api_key = 'api_key'
    yelp_api = YelpAPI(api_key, timeout_s=3.0)
    search_results = yelp_api.search_query(location='CA', limit=5, offset=offset)
    return search_results

def get_ca_businesses():
    businesses = get_businesses(0)
    n_bs = businesses['total']
    n_runs = n_bs // 50
    offset = 50
    bs_list = businesses['businesses']
    for i in range(0,n_runs):
        businesses = get_businesses(offset)
        bs_list.extend(businesses['businesses'])
        offset += 50

    for bs in list(bs_list):
        name = bs['name']
        url = get_wikipedia_url(name)
        rating = bs['rating']
        parking = check_parking(bs)
        weekends = open_weekends(bs['id'])
        location = bs['location']['city']
        user_data = get_user_reviews(bs['id'])
        update_business_db((name,rating,url,parking,weekends),location,user_data)

get_ca_businesses()
