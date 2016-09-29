from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.encoding import uri_to_iri
from .forms import CourseForm, TermForm
from get_access_token import get_access_token

import json
import requests
import urlparse
from urllib import urlencode
from pprint import pprint

DEBUG = False

config_file           = open('../configuration.json')
api_url, access_token = get_access_token(config_file)
headers               = {'Authorization': 'Bearer ' + access_token}


def get_term_code(year, term):
	if not year or not term:
		return None

	term_codes = {'fall': '01', 'winter': '02', 'spring': '03', 'summer': '04'}
	term_idx   = term_codes[term]
	if term == 'fall':
		year = int(year) + 1
	term_code  = str(year) + term_idx
	return term_code


def get_courses_url(request_url, term_code, subject, course_num, q, page_size, page_num):
	endpoint     = '/courses'
	request_url  += endpoint
	params       = {'term': term_code, 'subject': subject, 'courseNumber': course_num, 'q': q, 'page[size]': page_size, 'page[number]': page_num}
	url_parts    = list(urlparse.urlparse(request_url))
	query        = dict(urlparse.parse_qsl(url_parts[4]))
	query.update(params)
	url_parts[4] = urlencode(query)
	request_url  = urlparse.urlunparse(url_parts)

	return uri_to_iri(request_url)


def get_details(response):
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
	global config_file, api_url, access_token, headers
	request_url = api_url

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
		data, links = get_details(response)
	else:
		if DEBUG:
			print "Form is not valid."

	return render_to_response('catalog_api_demo/class_search_api_index.html', locals(), RequestContext(request))


def course_subjects_api(request):
	global config_file, api_url, access_token, headers
	endpoint    = '/subjects'
	request_url = api_url + endpoint

	response    = requests.get(request_url, headers=headers)
	data, links = get_details(response)
	return render_to_response('catalog_api_demo/course_subjects_api_index.html', locals(), RequestContext(request))


def get_term_url(request_url, term_code, is_open, page_size, page_num):
	endpoint    = '/terms'
	request_url += endpoint
	params      = {'page[size]': page_size, 'page[number]': page_num}

	if is_open:
		return request_url + '/open'
	if term_code:
		request_url += '/' + term_code

	url_parts    = list(urlparse.urlparse(request_url))
	query        = dict(urlparse.parse_qsl(url_parts[4]))
	query.update(params)
	url_parts[4] = urlencode(query)
	request_url  = urlparse.urlunparse(url_parts)

	return uri_to_iri(request_url)


def terms_api(request):
	global config_file, api_url, access_token, headers
	request_url = api_url

	form          = TermForm(request.POST)
	form_is_valid = form.is_valid()
	if form_is_valid:
		year        = form.cleaned_data['year']
		term        = form.cleaned_data['term']
		term_code   = get_term_code(year, term)
		is_open     = form.cleaned_data['is_open']
		page_size   = form.cleaned_data['page_size']
		page_num    = form.cleaned_data['page_num']
		request_url = get_term_url(request_url, term_code, is_open, page_size, page_num)
		response    = requests.get(request_url, headers=headers)
		data, links = get_details(response)
	else:
		if DEBUG:
			print "Form is not valid."

	return render_to_response('catalog_api_demo/terms_api_index.html', locals(), RequestContext(request))


def catalog_api(request):
	return render_to_response('catalog_api_demo/catalog_api_index.html', locals(), RequestContext(request))
