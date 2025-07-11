from rest_framework import serializers
from .models import Cuisine, Ingredient, Recipe, StepPicture, Favourite, Rating, RecipeIngredient

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id', 'name']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id','name', 'image']

class StepPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepPicture
        fields = ['id', 'image']

class RecipeSerializer(serializers.ModelSerializer):
    cuisine = serializers.UUIDField(write_only=True)
    ingredients = serializers.ListField(child=serializers.UUIDField(), write_only=True)
    step_pictures = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions',
            'prep_duration', 'cook_duration', 'thumbnail',
            'cuisine', 'ingredients', 'step_pictures'
        ]

    def create(self, validated_data):
        cuisine_id = validated_data.pop('cuisine')
        ingredient_ids = validated_data.pop('ingredients', [])
        step_picture_ids = validated_data.pop('step_pictures', [])

        recipe = Recipe.objects.create(
            creator=self.context['request'].user,
            cuisine_id=cuisine_id,
            **validated_data
        )

        for ingredient_id in ingredient_ids:
            RecipeIngredient.objects.create(recipe=recipe, ingredient_id=ingredient_id)
        
        recipe.step_pictures.set(step_picture_ids)
        return recipe
    
    def update(self, instance, validated_data):
        cuisine_id = validated_data.pop('cuisine', None)
        ingredient_ids = validated_data.pop('ingredients', None)
        step_picture_ids = validated_data.pop('step_pictures', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cuisine_id:
            instance.cuisine_id = cuisine_id

        if ingredient_ids is not None:
            instance.recipeingredient_set.all().delete()
            for ingredient_id in ingredient_ids:
                RecipeIngredient.objects.create(recipe=instance, ingredient_id=ingredient_id)

        if step_picture_ids is not None:
            instance.step_pictures.set(step_picture_ids)

        instance.save()
        return instance

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['id', 'user', 'recipe']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'recipe', 'score']

    def create(self, validated_data):
        user = self.context['request'].user
        rating, created = Rating.objects.update_or_create(
            user=user,
            recipe=validated_data['recipe'],
            defaults={'score': validated_data['score']}
        )
        return rating
    
class RecipeDetailSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    step_pictures = StepPictureSerializer(many=True)
    cuisine = CuisineSerializer()

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions',
            'prep_duration', 'cook_duration', 'thumbnail',
            'cuisine', 'ingredients', 'step_pictures'
        ]
