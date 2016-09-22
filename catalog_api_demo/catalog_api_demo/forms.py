from django import forms


class CourseForm(forms.Form):
	term = forms.CharField(label='term', max_length=100)
	subject = forms.CharField(label='subject', max_length=100)
	course_number = forms.CharField(label='course_number', max_length=100)
