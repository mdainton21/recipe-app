from django.urls import path
from .views import home, RecipeListView, RecipeDetailView

app_name = 'recipes'

urlpatterns = [
   path('', home),
   path('recipes/list/', RecipeListView.as_view(), name='list'),
   path('recipes/list/<pk>', RecipeDetailView.as_view(), name='detail')
]