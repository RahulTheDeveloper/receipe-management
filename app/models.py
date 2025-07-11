from django.db import models
import uuid
from users.models import CustomUser

class Cuisine(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)

class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='ingredient_images/')

class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    instructions = models.TextField()
    prep_duration = models.IntegerField(help_text="in minutes")
    cook_duration = models.IntegerField(help_text="in minutes")
    thumbnail = models.ImageField(upload_to='thumbnails/')
    step_pictures = models.ManyToManyField('StepPicture')

class RecipeIngredient(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

class StepPicture(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    image = models.ImageField(upload_to='step_pictures/')

class Favourite(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favourites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class Rating(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    score = models.IntegerField() 
