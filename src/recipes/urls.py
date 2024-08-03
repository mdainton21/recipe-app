from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, search, about, add_recipe

app_name = 'recipes'

urlpatterns = [
   path('', home),
   path('recipes/list/', RecipeListView.as_view(), name='list'),
   path('recipes/list/<pk>', RecipeDetailView.as_view(), name='detail'),
   path('recipes/search/', search, name='search'),
   path("recipes/add_recipe", add_recipe, name="add_recipe"),
   path("recipes/about/", about, name="about"),
]