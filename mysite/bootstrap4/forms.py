from django import forms

class NoColon(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(NoColon, self).__init__(*args, **kwargs)

class RecInputForm(NoColon):
    url = forms.URLField(label="Mountain Project URL:", max_length=100)
    latitude = forms.DecimalField(label="Latitude:", initial=33.8734, min_value=-90, max_value=90)
    longitude = forms.DecimalField(label="Longitude:", initial=-115.9010, min_value=-180, 
        max_value=180)
    max_distance = forms.IntegerField(label="Max Distance (mi):", initial=50, min_value=1)
    rec = forms.MultipleChoiceField(label="Recommenders:", choices=(
        ("top_pop", "Top Popular"),
        ('cosine_rec', 'Cosine Similarity'),
        ("debug", "Debug (show input)"),))
    num_recs = forms.IntegerField(label="Number of Recommendations:", initial=10, min_value=1)
    boulder_lower = forms.IntegerField(label="Lowest Boulder Grade: V", min_value=0, max_value=16, 
        initial=0)
    boulder_upper = forms.IntegerField(label="Highest Boulder Grade: V", min_value=0, max_value=16,
        initial=3)
    get_boulder = forms.BooleanField(label="Boulder:", initial=True, required=False)
    route_lower = forms.CharField(label="Lowest Route Grade: 5.", max_length=3, initial="8")
    route_upper = forms.CharField(label="Highest Route Grade: 5.", max_length=3, initial="10d")
    get_route = forms.BooleanField(label="Route:", initial=True, required=False)