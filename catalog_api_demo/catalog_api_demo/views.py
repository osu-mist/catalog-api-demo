from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import CourseForm

import json
import requests
from pprint import pprint

DEBUG = True


def get_access_token(token_url, client_id, client_secret):
	token_resp = requests.post(token_url, data={
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'client_credentials'})
	return token_resp.json()['access_token']


def get_term_code(year, term):
	if term == 'fall':
		year     = int(year) + 1
		term_idx = '01'
	elif term == 'winter':
		term_idx = '02'
	elif term == 'spring':
		term_idx = '03'
	elif term == 'summer':
		term_idx = '04'

	term_code = str(year) + term_idx
	return term_code


def get_courses_url(request_url, term_code, subject, course_num, q, page_size, page_num):
	endpoint    = '/courses'

	request_url += endpoint + '?term=' + term_code
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
	global DEBUG
	if response.status_code == 200:
		response_data  = response.json()['data']
		response_links = response.json()['links']
	else:
		response_data  = []
		response_links = []
	if DEBUG:
		pprint(json.loads(response.text))
	return response_data, response_links


def class_search_api(request):
	config_file   = open('../configuration.json')
	config_data   = json.load(config_file)
	base_url      = config_data['hostname'] + config_data['version'] + config_data['api']
	request_url   = base_url
	token_url     = base_url + config_data['token_endpoint']
	client_id     = config_data['client_id']
	client_secret = config_data['client_secret']
	access_token  = get_access_token(token_url, client_id, client_secret)
	headers       = {'Authorization': 'Bearer ' + access_token}

	form          = CourseForm(request.POST)
	form_is_valid = form.is_valid()
	if form_is_valid:
		year        = form.cleaned_data['year']
		term        = form.cleaned_data['term']
		term_code   = get_term_code(year, term)
		subject     = form.cleaned_data['subject']
		course_num  = form.cleaned_data['course_num']
		q           = form.cleaned_data['q']
		page_size   = form.cleaned_data['page_size']
		page_num    = form.cleaned_data['page_num']
		request_url = get_courses_url(request_url, term_code, subject, course_num, q, page_size, page_num)
		response    = requests.get(request_url, headers=headers)
		data, links = get_courses_details(response)
	else:
		if DEBUG:
			print "Form is not valid."

	return render_to_response('catalog_api_demo/class_search_api_index.html', locals(), RequestContext(request))
