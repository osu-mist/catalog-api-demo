from django.shortcuts import render_to_response

import json
import requests


def get_access_token():
	config_file = open("../configuration.json")
	config_data = json.load(config_file)

	base_url   = config_data["hostname"] + config_data["version"] + config_data["api"]
	token_url  = base_url + config_data["token_endpoint"]
	grant_type = "client_credentials"
	token_resp = requests.post(token_url, data={
		'client_id': config_data["client_id"],
		'client_secret': config_data["client_secret"],
		'grant_type': grant_type})
	return token_resp.json()['access_token']


def catalog_api_demo(request):
	print get_access_token()
	return render_to_response('catalog_api_demo.html')
