from django import forms
from .models import Recipe

SEARCH_CHOICES = [
    ("name", "Recipe Name"),
    ("cooking_time", "Cooking Time (minutes)"),
    ("difficulty", "Difficulty"),
]

class RecipeSearchForm(forms.Form):
    search_by = forms.ChoiceField(choices=SEARCH_CHOICES, required=True, label="Search by")
    search_term = forms.CharField(max_length=100, required=False, label="Search term")
    cooking_time = forms.IntegerField(required=False, label="Cooking Time (minutes)")
    difficulty = forms.ChoiceField(
        choices=[
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Intermediate", "Intermediate"),
            ("Hard", "Hard"),
        ],
        required=False,
        label="Difficulty"
    )

class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "name",
            "cooking_time",
            "ingredients",
            "description",
            "pic"
              ]