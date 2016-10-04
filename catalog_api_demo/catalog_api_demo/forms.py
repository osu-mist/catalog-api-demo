from django import forms


class CourseForm(forms.Form):
	term_choices = (('fall', 'Fall'), ('winter', 'Winter'), ('spring', 'Spring'), ('summer', 'Summer'))

	year       = forms.CharField(label='Year', required=True)
	term       = forms.ChoiceField(label='Term', widget=forms.RadioSelect, choices=term_choices, required=True)
	subject    = forms.CharField(label='Subject', required=False)
	course_num = forms.CharField(label='Course Number', required=False)
	q          = forms.CharField(label='Query', required=False)
	page_size  = forms.CharField(label='Page Size', required=False)
	page_num   = forms.CharField(label='Page Number', required=False)


class TermForm(forms.Form):
	term_choices = (('fall', 'Fall'), ('winter', 'Winter'), ('spring', 'Spring'), ('summer', 'Summer'), ('none', 'None'))

	year      = forms.CharField(label='Year', required=False)
	term      = forms.ChoiceField(label='Term', widget=forms.RadioSelect, choices=term_choices, required=False)
	is_open   = forms.BooleanField(label='Open', required=False)
	page_size = forms.CharField(label='Page Size', required=False)
	page_num  = forms.CharField(label='Page Number', required=False)
