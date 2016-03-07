from flask import Blueprint
from app import oauth

auth = Blueprint('auth', __name__)

facebook = oauth.remote_app(
    'facebook',
    consumer_key='449699711888450',
    consumer_secret='a968e17aeffb7d0c35ff22d5c7fc5a7f',
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)

twitter = oauth.remote_app(
    'twitter',
    consumer_key='XCHhGuDrxVuGzwX95vhyQv2LY',
    consumer_secret='9b0mwKWy1j3YKpAlaojorSCpBKE5eo9hIAcpTKJXS2VVOtB0HA',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
)



from . import views