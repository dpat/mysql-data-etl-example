from mysqlconnect import Mysqlconnect
from yelp import Yelpapiconnect
from helpers import check_parking, get_wikipedia_url


def update_location_table(location_name):
    # take existing id or create
    id = Mysqlconnect.sql_get_id('locations','location',location_name)
    if id is None:
        data = (location_name, )
        sql_call = "INSERT INTO locations (location) VALUES (%s)"
        Mysqlconnect.sql_insert(sql_call, data)
        id = Mysqlconnect.sql_get_id('locations','location',location_name)
    return id


def update_user_table(user_data):
    # take existing id or create
    yelp_id = user_data[0]
    user_url = user_data[1]
    id = Mysqlconnect.sql_get_id('users','yelp_user_id',yelp_id)
    if id is None:
        sql_call = "INSERT INTO users (yelp_user_id, user_url) VALUES (%s, %s)"
        Mysqlconnect.sql_insert(sql_call, user_data)
        id = Mysqlconnect.sql_get_id('users','yelp_user_id',yelp_id)
    return id


def update_business_db(business_data,location_data,user_data):
    loc_id = update_location_table(location_data)
    user_id = update_user_table(user_data)
    business_data = business_data + (loc_id, user_id,)
    sql_call = "INSERT INTO businesses(name, rating, wiki_url, parking, open_weekends, location_id, most_recent_review_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    Mysqlconnect.sql_insert(sql_call, business_data)


def get_ca_businesses():
    businesses = Yelpapiconnect.get_businesses(0)
    n_bs = businesses['total']
    n_runs = 10 #n_bs // 50 #10 for now as 1000 is max
    offset = 50
    bs_list = businesses['businesses']
    for i in range(0,n_runs):
        businesses = Yelpapiconnect.get_businesses(offset)
        bs_list.extend(businesses['businesses'])
        offset += 50

    for bs in list(bs_list):
        name = bs['name']
        url = get_wikipedia_url(name)
        rating = bs['rating']
        parking = check_parking(bs)
        weekends = Yelpapiconnect.open_weekends(bs['id'])
        location = bs['location']['city']
        user_data = Yelpapiconnect.get_user_reviews(bs['id'])
        update_business_db((name,rating,url,parking,weekends),location,user_data)

get_ca_businesses()
