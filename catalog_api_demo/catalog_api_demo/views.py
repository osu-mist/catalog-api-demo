from django.shortcuts import render_to_response


def here(request, a, b):
	return render_to_response('here.html', locals())
