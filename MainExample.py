import requests
import os 
import time
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
from InstagramWrapper import InstagramWrapper
from requests_oauthlib import OAuth2Session

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # this lets my redirect_uri be a non secure (http) URL, otherwise OAuth restricts you to HTTPS
# when we push to a server we'll obviously take this out.

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

instagram_client_id = "115a6c0fd0a64bccbf213e4eafec554a"
instagram_client_secret = "72f3282930444d9e826e5f083ede32d1"
instagram_authorization_base_url = "https://api.instagram.com/oauth/authorize"
instagram_token_url = "https://api.instagram.com/oauth/access_token"

@app.route('/')
def hello_world():
	oauth = OAuth2Session(instagram_client_id, redirect_uri="http://127.0.0.1:5000/callback")
	authorization_url, state = oauth.authorization_url(instagram_authorization_base_url)

	session['oauth_state'] = state
	return redirect(authorization_url)

@app.route('/callback', methods=["GET"])
def callback():
	oauth = OAuth2Session(instagram_client_id, redirect_uri="http://127.0.0.1:5000/callback", state=session['oauth_state'])
	# When grabbing the token Instagram requires you give the code you got in the authorization step in the token step, along with client_id + secret -_-
	# This fetch token call might not be right for other APIs, it all demands on their requirements
	my_token = oauth.fetch_token(instagram_token_url, code=request.args.get('code'), client_secret=instagram_client_secret, client_id=instagram_client_id, authorization_url=request.url)
	session['instagram_access_key'] = my_token['access_token']
	return jsonify(oauth.request("GET", "https://api.instagram.com/v1/users/self/?access_token=" + session['instagram_access_key']).json())
	

if __name__ == '__main__':
    app.run()
