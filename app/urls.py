from django.urls import path, include
from .views import *

urlpatterns = [
    path('create-receipe/', RecipeCreateView.as_view()),
    path('update-receipe/<uuid:pk>/', RecipeCreateView.as_view()),
    path('delete-receipe/', DeleteRecipeView.as_view()),
    path('upload-excel/', BulkRecipeUploadView.as_view()),
    
    path('create-ingredients/', IngredientCreateAPIView.as_view()),
    path('create-cuisine/', CuisineCreateAPIView.as_view()),
    path('create-step-picture/',StepPictureCreateAPIView.as_view()),
    
    path('create-favourites/', FavouriteView.as_view(), name='favourite-recipe'),   
    path('create-ratings/', RatingCreateView.as_view(), name='create-rating'), 
    
    path('list-recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('detail-recipe/<uuid:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe-pdf/', RecipePDFDownloadView.as_view()),
    
    path('cuisine-stats/', CuisineStatsView.as_view())
]