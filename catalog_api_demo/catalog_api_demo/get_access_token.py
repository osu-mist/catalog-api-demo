import requests
import json


def get_access_token(config_file):
	config_data   = json.load(config_file)
	api_url       = config_data['hostname'] + config_data['version'] + config_data['api']
	token_url     = api_url + config_data['token_endpoint']
	client_id     = config_data['client_id']
	client_secret = config_data['client_secret']

	token_resp = requests.post(token_url, data={
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'client_credentials'})
	return api_url, token_resp.json()['access_token']
