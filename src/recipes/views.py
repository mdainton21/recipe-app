from django.shortcuts import render
from django.views.generic import ListView, DetailView
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe

# Create your views here.

def home(request):
   return render(request, 'recipes/recipes_home.html')

#Use Listview for listing the recipes
class RecipeListView(LoginRequiredMixin, ListView):  
    model = Recipe  
    template_name = 'recipes/recipe_overview.html'

#Use DetailView for the individual recipe page
class RecipeDetailView(LoginRequiredMixin, DetailView): 
    model = Recipe
    template_name = 'recipes/recipe_detail.html'