from yelpapi import YelpAPI
from datetime import datetime


class Yelpapiconnect:

    api_key = 'api_key'
    yelp_api = YelpAPI(api_key, timeout_s=3.0)

    @classmethod
    def get_businesses(self, offset):
        search_results = self.yelp_api.search_query(location='CA', limit=5, offset=offset)
        return search_results

    @classmethod
    def get_user_reviews(self, business_id):
        reviews = self.yelp_api.reviews_query(id=business_id)
        review_list = reviews['reviews']
        most_recent_review = max(review_list, key=lambda x:datetime.strptime(x['time_created'], '%Y-%m-%d %H:%M:%S'))
        user_id = most_recent_review['user']['id']
        user_profile = most_recent_review['user']['profile_url']
        return (user_id, user_profile)


    @classmethod
    def open_weekends(self, business_id):
        business_result = self.yelp_api.business_query(id=business_id)
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
