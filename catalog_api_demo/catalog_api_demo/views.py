from django.shortcuts import render_to_response

import json
import requests


def get_access_token(token_url, client_id, client_secret):
	token_resp = requests.post(token_url, data={
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'client_credentials'})

	return token_resp.json()['access_token']


def catalog_api_demo(request):
	config_file   = open("../configuration.json")
	config_data   = json.load(config_file)
	base_url      = config_data['hostname'] + config_data['version'] + config_data['api']
	token_url     = base_url + config_data['token_endpoint']
	client_id     = config_data['client_id']
	client_secret = config_data['client_secret']
	access_token  = get_access_token(token_url, client_id, client_secret)

	headers = {'Authorization': 'Bearer ' + access_token}
	request_url = base_url + '/terms'
	response = requests.get(request_url, headers=headers).json()

	return render_to_response('catalog_api_demo.html', locals())
