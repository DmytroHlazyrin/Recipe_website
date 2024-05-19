from ajax_select.fields import AutoCompleteSelectMultipleField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from catalog.models import Cook, Dish, Composition, Category, Ingredient, Review


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


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['image', 'name', 'description', 'recipe', 'cooking_time', 'servings', 'calories', 'category']
        widgets = {
            'cooking_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),}

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()


class CompositionForm(forms.ModelForm):
    class Meta:
        model = Composition
        fields = ['ingredient', 'amount', 'measure']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }


CompositionFormSet = forms.inlineformset_factory(
    Dish,
    Composition,
    form=CompositionForm,
    extra=1,
    can_delete=True
)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_body']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review_body': forms.Textarea(attrs={'rows': 4}),
        }
