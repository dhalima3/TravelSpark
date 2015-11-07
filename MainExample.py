import requests
import os 
import time
import random
from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify
from requests_oauthlib import OAuth2Session

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
instagram_image_search_url = "https://api.instagram.com/v1/locations/search"

google_api_key = "AIzaSyCLehiRvLWhFXbwkI6zojampXcICC0-rMU"
google_geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s"


@app.route('/')
def instagram_authorization():
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
	if(session.get('instagram_access_key') == None):
		return redirect("/")
	#Lets get info on myself the access_token holder
	access_token = session['instagram_access_key']
	r = requests.request("GET",'https://api.instagram.com/v1/users/self/?access_token=%s' % access_token)
	return render_template('home.html', user_data=r.json())


'''
	The main route for the collage page
'''
@app.route('/location/<place>')
def get_photos_for_location(place):
	return None


'''
	Will return a list of image URLs from instagram given the name of a location
'''
@app.route('/location/instagram', methods=["POST"])
def get_instagram_photos():
	if(session.get('instagram_access_key') == None):
		return redirect("/")

	# Use Google Geocoding to convert place to lat and long coordinates
	place = request.form['place']
	location = requests.get(google_geocoding_url % place)
	location = location.json()
	lat_coord = location.get("results")[0].get("geometry").get("location").get("lat")
	long_coord = location.get("results")[0].get("geometry").get("location").get("lng")

	# Make the API call to get the Models
	querys = {"lat": lat_coord, "lng" : long_coord, "access_token" : session.get('instagram_access_key')}
	instagram_models = requests.get(instagram_image_search_url, params=querys)

	num_photos = int(request.form['num_photos'])
	photo_choices = []
        #for i in range(0, num_photos):

@app.route('/collage')
def get_collage():
    return render_template('collage.html')

if __name__ == '__main__':
    app.run()
