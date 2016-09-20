from django.shortcuts import render_to_response


def catalog_api_demo(request):
	return render_to_response('catalog_api_demo.html')
