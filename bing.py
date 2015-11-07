from flask import Flask
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

app = Flask(__name__)
app.secret_key="wefoiwef239042i34nfw0934223rjiofwo"
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

client_id = 'a8d67f03-9f4e-4a7a-b40d-4b85b83a575e'
client_secret='HiQXAcsztSiB63zqdrrBK+ClMcn+EF60rD0PmTMJrqQ='
authorization_base_url='https://login.microsoftonline.com/common/oauth2/authorize'
authorization_token_url='https://login.microsoftonline.com/common/oauth2/token'

@app.route('/')
def login():
	microsoft= OAuth2Session(client_id, redirect_uri='http://127.0.0.1:5000/response')
	authorization_url, state = microsoft.authorization_url(authorization_base_url)
	print authorization_url 
	session['oauth_state'] = state
	print state
	return redirect(authorization_url)

@app.route('/response', methods=["GET"]) 
def callback():
	microsoft=OAuth2Session(client_id, redirect_uri="http://127.0.0.1:5000/response", state=session['oauth_state'])
	token=microsoft.fetch_token(authorization_token_url, client_id= client_id, client_secret= client_secret, code=request.args.get('code'), grant_type="authorization_code", redirect_uri= microsoft.redirect_uri
		)
	print token

if __name__ == '__main__':
    app.run()
