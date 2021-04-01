from django import forms


class ImageThumbnailForm(forms.Form):
	w = forms.IntegerField(required=False, min_value=100, max_value=1920)
	h = forms.IntegerField(required=False, min_value=100, max_value=1080)

	def clean(self):
		cleaned_data = super(ImageThumbnailForm, self).clean()

		max_width = cleaned_data.get('w')
		max_height = cleaned_data.get('h')

		cleaned_data['max_width'] = max_width
		cleaned_data['max_height'] = max_height

		return cleaned_data