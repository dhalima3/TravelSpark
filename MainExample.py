import requests
import os 
import time
import random
from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify, dumps, loads
from requests_oauthlib import OAuth2Session
import requests
import json


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, tmpl_dir)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

instagram_client_id = "115a6c0fd0a64bccbf213e4eafec554a"
instagram_client_secret = "72f3282930444d9e826e5f083ede32d1"
instagram_authorization_base_url = "https://api.instagram.com/oauth/authorize"
instagram_token_url = "https://api.instagram.com/oauth/access_token"
instagram_image_search_url = "https://api.instagram.com/v1/media/search"

google_api_key = "AIzaSyCLehiRvLWhFXbwkI6zojampXcICC0-rMU"
google_geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s"


@app.route('/')
def instagram_authorization():
	if(session.get("instagram_access_key" != None)):
		return redirect("/home")

	oauth = OAuth2Session(instagram_client_id, redirect_uri="http://127.0.0.1:5000/callback")
	authorization_url, state = oauth.authorization_url(instagram_authorization_base_url)

	session['oauth_state'] = state
	return redirect(authorization_url)

@app.route('/callback', methods=["GET"])
def instagram_token_retrieval():
	oauth = OAuth2Session(instagram_client_id, redirect_uri="http://127.0.0.1:5000/callback", state=session['oauth_state'])
	# When grabbing the token Instagram requires you give the code you got in the authorization step in the token step, along with client_id + secret -_-
	# This fetch token call might not be right for other APIs, it all demands on their requirements
	my_token = oauth.fetch_token(instagram_token_url, code=request.args.get('code'), client_secret=instagram_client_secret, client_id=instagram_client_id, authorization_url=request.url)
	session['instagram_access_key'] = my_token['access_token']
	return redirect("/home")

'''
	Route representing the home page
'''
@app.route('/home')
def home():
	#TODO: Put in Flickr APi for the home page. 
	if(session.get('instagram_access_key') == None):
		return redirect("/")
	#Lets get info on myself the access_token holder
	access_token = session['instagram_access_key']
	r = requests.request("GET",'https://api.instagram.com/v1/users/self/?access_token=%s' % access_token)
	return render_template('home.html', user_data=r.json())


'''
	The main route for the collage page
'''
#after user hits submit button. 
@app.route('/location/<place>')
def get_collage(place):
	#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	#payload = {'num_photos': 3, 'place': place}
	url = 'http://127.0.0.1:5000/location/instagram/'+place
	#import urlparse
	#url = 'http://127.0.0.1:5000/location/instagram/holder'
	#parts = urlparse.urlparse(url)
	#parts = parts._replace(path=)
	#parts.geturl()
	#print payload
	response = get_instagram_photos(place)
        price = "Fares as low as " + str(get_lowest_price(place))
	print "RECIEVES"
	print response
    	return render_template('collage.html', photos_display=response, lowest_price=price)

def get_lowest_price(place):
    f = open('./jetblue/jetblueresults', 'r')
    place = place.lower().replace("+", " ")
    for line in f:
        lineList = line.split(',')
        destination = lineList[2].lower()
        if (destination == place.lower()):
            return lineList[4]
        
'''
	Will return a list of image URLs from instagram given the name of a location
'''

def get_instagram_photos(place):
	print "hell"
	if(session.get('instagram_access_key') == None):
		print "REDIRECT"
		return redirect("/")
    #http://127.0.0.1:5000/location/instagram/Chicago/3
    #place, num_photos, 
	# Use Google Geocoding to convert place to lat and long coordinates
	num_photos = 19;
	print place
	location = requests.get(google_geocoding_url % place)
	location = location.json()
	print location
	lat_coord = location.get("results")[0].get("geometry").get("location").get("lat")
	long_coord = location.get("results")[0].get("geometry").get("location").get("lng")
	print lat_coord
	print long_coord
	# Make the API call to get the Models
	querys = {"lat": lat_coord, "lng" : long_coord,  "distance" : "10000" , "access_token": session.get('instagram_access_key')}
	instagram_models = requests.get(instagram_image_search_url, params=querys)
	chosen_images = []

	json_object = loads(instagram_models.text) 
	print json_object
	if len(json_object["data"]) > num_photos:
		for i in range(0, num_photos): 
			chosen_images.append(json_object["data"][i]["images"])
	else:
		print len(json_object["data"])
		print num_photos

	print chosen_images
	return chosen_images		




if __name__ == '__main__':
	app.run()
