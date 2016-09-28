from django import forms


class CourseForm(forms.Form):
	year       = forms.CharField(label='year', required=True)
	term       = forms.CharField(label='term', required=True)
	subject    = forms.CharField(label='subject', required=False)
	course_num = forms.CharField(label='course_num', required=False)
	q          = forms.CharField(label='q', required=False)
	page_size  = forms.CharField(label='page_size', required=False)
	page_num   = forms.CharField(label='page_num', required=False)


class TermForm(forms.Form):
	year      = forms.CharField(label='year', required=False)
	term      = forms.CharField(label='term', required=False)
	is_open   = forms.CharField(label='is_open', required=False)
	page_size = forms.CharField(label='page_size', required=False)
	page_num  = forms.CharField(label='page_num', required=False)
