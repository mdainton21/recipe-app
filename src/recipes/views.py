from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Recipe
import pandas as pd
from .forms import RecipeSearchForm, NewRecipeForm
from .utils import get_chart


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

#About me page
def about(request):
    return render(request, "recipes/about_me.html")


@login_required
def search(request):
    # adds an instance of RecipesSearchForm
    form = RecipeSearchForm(request.POST or None)

    # Initializes dataframe to None
    recipes_df = None

    bar_chart = None
    pie_chart = None
    line_chart = None

    if request.method == "POST" and form.is_valid():
        # Retrieves the search criteria from the form
        search_by = form.cleaned_data.get("search_by")
        search_term = form.cleaned_data.get("search_term")
        cooking_time = form.cleaned_data.get("cooking_time")
        difficulty = form.cleaned_data.get("difficulty")

        # Filters the queryset based on the form input
        qs = Recipe.objects.all()

        if search_by == "name" and search_term:
            qs = qs.filter(name__icontains=search_term)
        elif search_by == "cooking_time" and cooking_time is not None:
            qs = qs.filter(cooking_time=cooking_time)
        elif search_by == "difficulty" and difficulty:
            qs = [recipe for recipe in qs if recipe.difficulty == difficulty]

        # Checks if the queryset is not empty
        if qs:
            # Converts list to pandas dataframe, else converts queryset to pandas DataFrame
            if isinstance(qs, list):
                recipes_df = pd.DataFrame([recipe.__dict__ for recipe in qs])
            else:
                recipes_df = pd.DataFrame(qs.values())

            recipes_df.index += 1

            # Retrieves each Recipe object using its id, then calls get_absolute_url() on it to generate the link
            def format_recipe_name_table(row):
                recipe = Recipe.objects.get(id=row["id"])
                return f"<a href='{recipe.get_absolute_url()}'>{row['name']}</a>"
            
            def format_recipe_name_chart(row):
                return row["name"]

            recipes_df["name_table"] = recipes_df.apply(format_recipe_name_table, axis=1)
            recipes_df["name_chart"] = recipes_df.apply(format_recipe_name_chart, axis=1)

            # Calculates difficulty and number of ingredients for each recipe
            recipes_df["difficulty"] = [recipe.difficulty for recipe in qs]
            recipes_df["number_of_ingredients"] = recipes_df["ingredients"].apply(lambda x: len(x.split(", ")))

            # Generate charts
            bar_chart = get_chart("#1", recipes_df, labels=recipes_df["name_chart"].values)
            pie_chart = get_chart("#2", recipes_df, labels=recipes_df["difficulty"].values)
            line_chart = get_chart("#3", recipes_df, labels=recipes_df["name_chart"].values)

            recipes_df = recipes_df[["name_table", "cooking_time", "difficulty"]]
            recipes_df = recipes_df.rename(columns={"name_table": "Name"})
            recipes_df = recipes_df.rename(columns={"cooking_time": "Cooking Time (minutes)"})
            recipes_df.columns = recipes_df.columns.str.capitalize()

            # Convert DataFrame to HTML for display
            recipes_df = recipes_df.to_html(escape=False)


    # Prepares data to send from view to template
    context = {
        "form": form,
        "recipes_df": recipes_df,
        "bar_chart": bar_chart,
        "pie_chart": pie_chart,
        "line_chart": line_chart,
    }

    # Loads page using "context" information
    return render(request, "recipes/recipe_search.html", context)

@login_required
def add_recipe(request):

    if request.method == "POST":
        new_recipe_form = NewRecipeForm(request.POST, request.FILES)

        if new_recipe_form.is_valid():
            new_recipe_form.save()
            return redirect("recipes:list")
        
    else:
        new_recipe_form = NewRecipeForm()

    context = {
        "new_recipe_form": new_recipe_form
    }

    return render(request, "recipes/add_recipe.html", context)