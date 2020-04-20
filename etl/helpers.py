import wikipedia


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
