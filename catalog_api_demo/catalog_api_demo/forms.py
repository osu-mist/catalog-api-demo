from django import forms


class CourseForm(forms.Form):
	term       = forms.CharField(label='term', max_length=100)
	subject    = forms.CharField(label='subject', max_length=100)
	course_num = forms.CharField(label='course_num', max_length=100)
	q          = forms.CharField(label='q', max_length=100)
	page_size  = forms.CharField(label='page_size', max_length=100)
	page_num   = forms.CharField(label='page_num', max_length=100)
