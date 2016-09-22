from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import CourseForm

import json
import requests


def get_access_token(token_url, client_id, client_secret):
	token_resp = requests.post(token_url, data={
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'client_credentials'})
	return token_resp.json()['access_token']


def catalog_api_demo(request):
	config_file   = open('../configuration.json')
	config_data   = json.load(config_file)
	base_url      = config_data['hostname'] + config_data['version'] + config_data['api']
	request_url   = base_url
	token_url     = base_url + config_data['token_endpoint']
	client_id     = config_data['client_id']
	client_secret = config_data['client_secret']
	access_token  = get_access_token(token_url, client_id, client_secret)
	headers       = {'Authorization': 'Bearer ' + access_token}

	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			term       = form.cleaned_data['term']
			subject    = form.cleaned_data['subject']
			course_num = form.cleaned_data['course_num']
			q          = form.cleaned_data['q']
			page_size  = form.cleaned_data['page_size']
			page_num   = form.cleaned_data['page_num']
			request_url += '/courses?term=' + term + '&subject=' + subject + '&courseNumber=' + course_num + '&q=' + q + '&page[size]=' + page_size + '&page[num]=' + page_num
	response = requests.get(request_url, headers=headers).json()
	return render_to_response('catalog_api_demo.html', locals(), RequestContext(request))
