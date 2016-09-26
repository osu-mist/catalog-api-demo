from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import CourseForm

import json
import requests
from pprint import pprint


def get_access_token(token_url, client_id, client_secret):
	token_resp = requests.post(token_url, data={
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'client_credentials'})
	return token_resp.json()['access_token']


def get_courses_url(request_url, term, subject, course_num, q, page_size, page_num):
	endpoint    = '/courses'
	request_url += endpoint + '?term=' + term
	if subject != '':
		request_url += '&subject=' + subject
	if course_num != '':
		request_url += '&courseNumber=' + course_num
	if q != '':
		request_url += '&q=' + q
	if page_size != '':
		request_url += '&page[size]=' + page_size
	if page_num != '':
		request_url += '&page[number]=' + page_num
	return request_url


def get_courses_details(response):
	response_data  = response.json()['data']
	response_links = response.json()['links']
	pprint(json.loads(response.text))
	return response_data, response_links


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

	form = CourseForm(request.POST)
	if form.is_valid():
		term        = form.cleaned_data['term']
		subject     = form.cleaned_data['subject']
		course_num  = form.cleaned_data['course_num']
		q           = form.cleaned_data['q']
		page_size   = form.cleaned_data['page_size']
		page_num    = form.cleaned_data['page_num']
		request_url = get_courses_url(request_url, term, subject, course_num, q, page_size, page_num)
	else:
		print "Form is not valid."
	response    = requests.get(request_url, headers=headers)
	data, links = get_courses_details(response)

	return render_to_response('catalog_api_demo/index.html', locals(), RequestContext(request))
