from flask import Flask
from instagram.client import InstagramAPI
from instagram.models import Media
import simplejson

app = Flask(__name__)


access_token = "222186701.a1dbb86.a695fe190bd44ed1ac4ef62608ba5b38"
client_secret = "c38046f2f8ff49a8b646717305a6efd0"
image_ids = []

@app.route('/')
def images_display():
    api = InstagramAPI(access_token=access_token, client_secret=client_secret)
    json_locations = api.media_search(lat=55.770968, lng=38.680028,
                                      min_timestamp=None, max_timestamp=None, distance=5000)

    html_code = '''<html><body>'''
    for media in json_locations:
        html_code += '''<img src=''' + media.images['standard_resolution'].url + ''' alt=''' + media.id + '''>'''
    html_code += '''</body></html>'''

    return html_code

@app.route('/images')
def images_json():
    api = InstagramAPI(access_token=access_token, client_secret=client_secret)
    json_locations = api.media_search(lat=55.770968, lng=38.680028,
                                      min_timestamp=None, max_timestamp=None, distance=5000)

    images = {}
    for media in json_locations:
        images[media.id] = media.images['standard_resolution'].url

    return simplejson.dumps(images)

@app.route('/geo')
def images_geo_json():
    api = InstagramAPI(access_token=access_token, client_secret=client_secret)
    json_locations = api.location_search(q=5000, count=None, lat=55.770968, lng=38.680028,
                                         foursquare_id=None, foursquare_v2_id=None)


    html_code = '''<html><body>'''
    for location in json_locations:
        media = api.location_recent_media(5, None, location.id)
        for element in media:
            if isinstance(element, list):
                html_code += images_geo(element, html_code, location.id)
            elif isinstance(element, Media):
                if image_ids.count(element.id) == 0:
                    image_ids.append(element.id)
                    html_code += '''<img src=''' + element.images['standard_resolution'].url \
                                 + ''' alt=''' + location.id + '''>'''

    html_code += '''</body></html>'''

    print image_ids
    print html_code
    return html_code


def images_geo(media_list, html, location_id):
    for element in media_list:
        if element is list:
            print "Something strange"
        elif isinstance(element, Media):
            if element.id not in image_ids:
                html += '''<img src=''' + element.images['standard_resolution'].url\
                        + ''' alt=''' + location_id + '''>'''
        else:
            print "type of e: "
            print type(element)
            print "e is: "
            print element
    return html


if __name__ == '__main__':
    app.run()
