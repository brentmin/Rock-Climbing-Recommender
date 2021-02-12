from django import forms

class RecInputForm(forms.Form):
    url = forms.URLField(label="Mountain Project URL", max_length=100)
    latitude = forms.DecimalField(label="Latitude", initial=33.8734)
    longitude = forms.DecimalField(label="Longitude", initial=-115.9010)
    rec = forms.MultipleChoiceField(label="Recommenders", choices=(
        ("top_pop", "Top Popular"),
        ("other", "Other Recommender")))