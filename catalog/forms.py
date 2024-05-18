from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from catalog.models import Cook


class CategorySearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        )
    )


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by username"}
        )
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Name or ingredient"}
        )
    )


class CookCreationForm(UserCreationForm):
    class Meta:
        model = Cook
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar')


class CookForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar')

