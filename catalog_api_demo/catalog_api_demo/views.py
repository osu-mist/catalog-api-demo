from django.shortcuts import render
from django.template import RequestContext
from django.utils.encoding import uri_to_iri
from django.views.decorators.csrf import csrf_protect
from .forms import *
from get_access_token import get_access_token

import json
import re
import requests
import urlparse
from urllib import urlencode
from pprint import pprint

DEBUG = False

config_file           = open('../configuration.json')
api_url, access_token = get_access_token(config_file)
headers               = {'Authorization': 'Bearer ' + access_token}


def encode_term_code(year, term):
	if not year:
		return None
	term_codes = {'fall': '01', 'winter': '02', 'spring': '03', 'summer': '04'}
	term_idx   = term_codes[term]
	year       = str(int(year) + 1) if term == 'fall' else year
	term_code  = str(year) + term_idx
	return term_code


def decode_term_code(termcode):
	if not termcode:
		return None, None
	term_codes = {'01': 'fall', '02': 'winter', '03': 'spring', '04': 'summer'}
	term       = term_codes[termcode[4:6]]
	year       = str(int(termcode[0:4]) - 1) if term == 'fall' else termcode[0:4]
	return year, term


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
	if type(response_data) is dict:
		response_data = [response_data]
	return response_data, response_links


@csrf_protect
def class_search_api(request):
	global config_file, api_url, access_token, headers
	request_url = api_url
	data, links = None, None

	form          = CourseForm(request.GET)
	form_is_valid = form.is_valid()
	if form_is_valid:
		year        = form.cleaned_data['year']
		term        = form.cleaned_data['term']
		term_code   = encode_term_code(year, term)
		subject     = form.cleaned_data['subject'].upper()
		course_num  = form.cleaned_data['course_num']
		q           = form.cleaned_data['q']
		page_size   = form.cleaned_data['page_size']
		page_num    = form.cleaned_data['page_num']
		request_url = get_courses_url(request_url, term_code, subject, course_num, q, page_size, page_num)
		response    = requests.get(request_url, headers=headers)
		data, links = get_details(response)
		if links:
			total_page   = re.findall(r'page\[number\]=(\d+)', uri_to_iri(links['last']))[0]
			current_page = re.findall(r'page\[number\]=(\d+)', uri_to_iri(links['self']))[0]
	else:
		if DEBUG:
			print "Form is not valid."

	page_form = PageForm(request.GET)
	if page_form.is_valid():
		page_link   = uri_to_iri(page_form.cleaned_data['page_link'])
		request_url = 'https://oregonstateuniversity-dev.apigee.net/' + re.findall(r'^https://api.oregonstate.edu/(.*)', page_link)[0]  # should be fixed in backend API
		params      = urlparse.parse_qs(urlparse.urlparse(request_url).query)
		termcode    = re.findall(r'^' + re.escape(api_url) + '/(\d)*', request_url)[0]
		year, term  = decode_term_code(termcode)
		subject     = params['subject'][0]
		course_num  = params['courseNumber'][0] if 'courseNumber' in params else None
		q           = params['q'][0] if 'q' in params else None
		page_size   = params['page[size]'][0]
		page_num    = params['page[number]'][0]
		response    = requests.get(request_url, headers=headers)
		data, links = get_details(response)
	else:
		render(request, 'catalog_api_demo/terms_api_index.html', locals())

	if links:
		total_page   = re.findall(r'page\[number\]=(\d+)', uri_to_iri(links['last']))[0]
		current_page = re.findall(r'page\[number\]=(\d+)', uri_to_iri(links['self']))[0]

	return render(request, 'catalog_api_demo/class_search_api_index.html', locals(), {'form': form})


def course_subjects_api(request):
	global config_file, api_url, access_token, headers
	endpoint    = '/subjects'
	request_url = api_url + endpoint

	response    = requests.get(request_url, headers=headers)
	data, links = get_details(response)
	return render(request, 'catalog_api_demo/course_subjects_api_index.html', locals())


def get_term_url(request_url, term_code, is_all, is_open, page_size, page_num):
	endpoint    = '/terms'
	request_url += endpoint
	params      = {'page[size]': page_size, 'page[number]': page_num}

	if is_all:
		request_url = request_url
	elif is_open:
		request_url += '/open'
	elif term_code:
		request_url += '/' + term_code

	url_parts    = list(urlparse.urlparse(request_url))
	query        = dict(urlparse.parse_qsl(url_parts[4]))
	query.update(params)
	url_parts[4] = urlencode(query)
	request_url  = urlparse.urlunparse(url_parts)

	return uri_to_iri(request_url)


@csrf_protect
def terms_api(request):
	global config_file, api_url, access_token, headers
	request_url = api_url
	data, links = None, None

	form          = TermForm(request.GET)
	form_is_valid = form.is_valid()
	if form_is_valid:
		year        = form.cleaned_data['year']
		term        = form.cleaned_data['term']
		term_code   = encode_term_code(year, term)
		is_all      = form.cleaned_data['is_all']
		is_open     = form.cleaned_data['is_open']
		page_size   = form.cleaned_data['page_size']
		page_num    = form.cleaned_data['page_num']
		request_url = get_term_url(request_url, term_code, is_all, is_open, page_size, page_num)
		response    = requests.get(request_url, headers=headers)
		data, links = get_details(response)
		if links:
			total_page   = re.findall(r'page\[number\]=(\d+)', uri_to_iri(links['last']))[0]
			current_page = re.findall(r'page\[number\]=(\d+)', uri_to_iri(links['self']))[0]
	else:
		if DEBUG:
			print "Form is not valid."

	page_form = PageForm(request.GET)
	if page_form.is_valid():
		page_link   = uri_to_iri(page_form.cleaned_data['page_link'])
		request_url = 'https://oregonstateuniversity-dev.apigee.net/' + re.findall(r'^https://api.oregonstate.edu/(.*)', page_link)[0]  # should be fixed in backend API
		params      = urlparse.parse_qs(urlparse.urlparse(request_url).query)
		is_all      = True if re.match(r'^' + re.escape(api_url) + '/terms\?', request_url) else False
		is_open     = True if re.match(r'^' + re.escape(api_url) + '/terms/open\?', request_url) else False
		termcode    = re.findall(r'^' + re.escape(api_url) + '/terms(\d)*', request_url)[0]
		year, term  = decode_term_code(termcode)
		page_size   = params['page[size]'][0]
		page_num    = params['page[number]'][0]
		response    = requests.get(request_url, headers=headers)
		data, links = get_details(response)
	else:
		return render(request, 'catalog_api_demo/terms_api_index.html', locals(), {'form': form})

	if links:
		total_page   = re.findall(r'page\[number\]=(\d+)', uri_to_iri(links['last']))[0]
		current_page = re.findall(r'page\[number\]=(\d+)', uri_to_iri(links['self']))[0]

	return render(request, 'catalog_api_demo/terms_api_index.html', locals(), {'form': page_form})


def catalog_api(request):
	return render(request, 'catalog_api_demo/catalog_api_index.html', locals())
