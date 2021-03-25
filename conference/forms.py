from django import forms


class AccessibilitySettingsForm(forms.Form):
	font_size_multiplier = forms.IntegerField(
		required=True,
		initial=1,
		widget=forms.NumberInput(attrs={
			"step": .1,
			"min": .5,
			"max": 3,
			"cols": 3,
			"style": "width:70px;",
		}),
		help_text=""
	)
	high_contrast_mode = forms.BooleanField(required=False, initial=False)
	text_to_speech = forms.BooleanField(required=False, initial=False, help_text="Narrate text on focus or on hover.")
