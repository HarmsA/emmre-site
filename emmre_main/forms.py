from django import forms
from django.forms import ModelForm
from .models import Blog, Tag, Category, Comment, PricePlan, FAQ


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


class BlogForm(forms.ModelForm):
	class Meta:
		model = Blog
		fields = '__all__'


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('author', 'text')


