import requests
import os 
import time
import random
from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify, dumps, loads
from requests_oauthlib import OAuth2Session
import requests
import json
import urllib2
import mechanize
from bs4 import BeautifulSoup
from urlparse import urlparse
from apiclient.discovery import build



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
@app.route('/location/<place>', methods=["POST", "GET"])
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

	response2= get_google_images(place)
	print "RECIEVES"
	print response
	print "GOOGLE"
	print response2
        place = place.replace("+", " ")
        airport = get_airport(place)
        price = "Packages for Jetblue start as low as " + str(get_lowest_price(place)) + ". "
        average_savings = "And save up to " + str(get_savings_percentage(place)) + " compared to Expedia! Wow Jetblue is so awesome!"
    	return render_template('collage.html', place=place, photos_display=response, photos_google= response2, lowest_price=price, average_savings=average_savings, airport=airport)

def get_airport(place):
    f = open('./jetblue/jetblueresults', 'r')
    for line in f:
        lineList = line.split(',')
        destination = lineList[2].lower()
        if (destination == place.lower()):
            return lineList[1]


def get_savings_percentage(place):
    f = open('./jetblue/jetblueresults', 'r')
    for line in f:
        lineList = line.split(',')
        destination = lineList[2].lower()
        if (destination == place.lower()):
            return lineList[5][:-1]

def get_lowest_price(place):
    f = open('./jetblue/jetblueresults', 'r')
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
	num_photos = 25;
	print place
	location = requests.get(google_geocoding_url % place)
	location = location.json()
	print location
	lat_coord = location.get("results")[0].get("geometry").get("location").get("lat")
	long_coord = location.get("results")[0].get("geometry").get("location").get("lng")
	print lat_coord
	print long_coord
	# Make the API call to get the Models
	querys = {"lat": lat_coord, "lng" : long_coord, "min_timestamp": "1262304000", "max_timestamp":"1446940800", "distance" : "10000" , "access_token": session.get('instagram_access_key')}
	instagram_models = requests.get(instagram_image_search_url, params=querys)
	chosen_images = []

	json_object = loads(instagram_models.text) 
	print json_object
	if len(json_object["data"]) > num_photos:
		for i in range(0, num_photos): 
			chosen_images.append(json_object["data"][i]["images"])
	else:
		for i in range(0, len(json_object["data"])):
			chosen_images.append(json_object["data"][i]["images"])
		print len(json_object["data"])
		print num_photos

	print chosen_images


	return chosen_images		

def get_google_images(place):
    print "MOVING ON TO GOOGLE"
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+place)
    print url
    req = urllib2.Request(url, headers={'accept': '*/*'})
    response = urllib2.urlopen(req)
    print "GOOGLE RESPONSE"
    print type(response)
    print "TYPE OF RESPONSE.READ"    
    ret = response.read()
    print len(ret)
    print "RET"
    print ret
    return ret


if __name__ == '__main__':
	app.run()
