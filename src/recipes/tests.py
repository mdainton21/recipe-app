from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeSearchForm


# Create your tests here.

class MyRecipeTest(TestCase):

    def setUpTestData():
        Recipe.objects.create(
            name= 'Waffles',
            cooking_time= 10,
            ingredients= 'Waffle Mix, Milk, Eggs, Butter, Syrup',
            description= 'Waffles are a small batter cake, baked in a waffle iron.'
            )
    
    #Tests to see if name length is too long
    def test_name_length(self):
        #Get the recipe data to test
        recipe = Recipe.objects.get(id=1)

        #Get the metadata for the 'name' field
        name_max_length = recipe._meta.get_field('name').max_length

        #Check to make sure it is shorter than max length
        self.assertEqual(name_max_length, 50)


    #Tests to see if the recipe name matches
    def test_name_status(self):
        #Get the recipe data to test
        recipe = Recipe.objects.get(id=1)

        #Get the metadata for the 'name' field
        field_name = recipe._meta.get_field('name').verbose_name

        #Check to make sure names match
        self.assertEqual(field_name, 'name')


    #Checks if cooking time matches
    def test_cooking_time_status(self):
        #Get the recipe data to test
        recipe = Recipe.objects.get(id=1)

        #Get the metadata for the 'cooking_time' field
        cooking_time_status = recipe._meta.get_field('cooking_time').help_text

        #Check to make sure the cooking time matches
        self.assertEqual(cooking_time_status, 'In minutes')


    #Checks if ingredients list is too long
    def test_ingredients_max_length(self):
        #Get the recipe data to test
        recipe = Recipe.objects.get(id=1)

        #Get the metadata for the 'ingredients' field
        max_length = recipe._meta.get_field("ingredients").max_length

        #Check to make sure it is shorter than max length
        self.assertEqual(max_length, 225)


    #Checks if difficulty matches
    def test_calculate_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.difficulty, "Hard")


    #Checks that link goes to correct location
    def test_get_absolute_url(self):
        # get absolute_url 
        recipe = Recipe.objects.get(id=1)
        # Loads url /recipes/list/1
        self.assertEqual(recipe.get_absolute_url(), '/recipes/list/1')

    #Test for Login
    def test_login_list(self):
        # Log in a fake user
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        
        #Check if they can acess the list page
        response = self.client.get(reverse("recipes:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_overview.html")

    #Test for Login #2
    def test_login_list(self):
        # Log in a fake user
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        
        #Check if they can acess the list page
        response = self.client.get(reverse("recipes:add_recipe"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/add_recipe.html")

    def test_search_form_validate(self):
        form = RecipeSearchForm(data={
            "search_by": "name",
            "search_term": "Test Recipe",
            "cooking_time": "",
            "difficulty": "",
        })

        #Checks if form is valid
        self.assertTrue(form.is_valid())

    def test_search_form_invalid_data(self):
        #Create invalid recipe data
        form = RecipeSearchForm(data={})

        # Checks if form is invalid
        self.assertFalse(form.is_valid())
    