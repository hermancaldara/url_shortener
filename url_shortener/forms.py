from django import forms


class ShortenURLForm(forms.Form):
    url = forms.URLField(
        label='URL',
        widget=forms.TextInput(attrs={'placeholder': 'Put a link to short it'})
    )
