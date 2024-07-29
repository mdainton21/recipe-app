from django.test import TestCase
from .models import Recipe

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

    