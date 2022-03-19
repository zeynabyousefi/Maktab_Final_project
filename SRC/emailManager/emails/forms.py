from django import forms


class SearchBox(forms.Form):
    search = forms.CharField()
