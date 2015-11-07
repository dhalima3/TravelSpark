import requests
import os 
import time
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

@app.route('/home')
def home():
	#Lets get info on myself the access_token holder
	access_token = session['instagram_access_key']
	r = requests.request("GET",'https://api.instagram.com/v1/users/self/?access_token=%s' % access_token)
	return render_template('home.html', user_data=r.json())


	

if __name__ == '__main__':
    app.run()
