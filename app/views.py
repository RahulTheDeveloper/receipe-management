from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg
from .models import Recipe, Favourite, Rating, Cuisine
from .serializers import RecipeSerializer, FavouriteSerializer, RatingSerializer, CuisineSerializer, IngredientSerializer, StepPictureSerializer
from users.permissions import *
from rest_framework.pagination import LimitOffsetPagination
from .serializers import RecipeDetailSerializer
from .tasks import process_bulk_recipes
import uuid
import os
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa



class RecipeCreateView(APIView):
    permission_classes = [IsCreatorOrReadOnly]

    def post(self, request):
        serializer = RecipeSerializer(data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        pk = request.query_params.get('pk')
        if not pk:
            return Response({'error': 'Missing pk'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = Recipe.objects.get(pk=pk, creator=request.user)
        except Recipe.DoesNotExist:
            return Response({'error': 'Not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RecipeSerializer(recipe, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DeleteRecipeView(APIView):
    permission_classes = [IsCreatorOrReadOnly]

    def delete(self, request):
        recipe_id = request.query_params.get('id')
        if not recipe_id:
            return Response({'error': 'Missing id query parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = Recipe.objects.get(pk=recipe_id, creator=request.user)
        except Recipe.DoesNotExist:
            return Response({'error': 'Not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

        recipe.delete()
        return Response({'message': 'Recipe deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    
class IngredientCreateAPIView(APIView):
    permission_classes = [IsCreator]

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            ingredient = serializer.save()
            return Response({
                'message': 'Ingredient created successfully',
                'data': IngredientSerializer(ingredient).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
class CuisineCreateAPIView(APIView):
    permission_classes = [IsCreator]

    def post(self, request):
        serializer = CuisineSerializer(data=request.data)
        if serializer.is_valid():
            cuisine = serializer.save()
            return Response({
                'message': 'Cuisine created successfully',
                'data': CuisineSerializer(cuisine).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StepPictureCreateAPIView(APIView):
    permission_classes = [IsCreator]

    def post(self, request):
        serializer = StepPictureSerializer(data=request.data)
        if serializer.is_valid():
            step_picture = serializer.save()
            return Response({
                'message': 'Step picture uploaded successfully',
                'data': StepPictureSerializer(step_picture).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class FavouriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipe_id = request.query_params.get('recipe_id')
        if not recipe_id:
            return Response({'error': 'Missing recipe_id query parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        Favourite.objects.get_or_create(user=request.user, recipe=recipe)
        return Response({'status': 'added to favourites'})

    def delete(self, request):
        recipe_id = request.query_params.get('recipe_id')
        if not recipe_id:
            return Response({'error': 'Missing recipe_id query parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        
        Favourite.objects.filter(user=request.user, recipe_id=recipe_id).delete()
        return Response({'status': 'removed from favourites'})


class RatingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RatingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecipeListView(APIView):
    def get(self, request):
        recipes = Recipe.objects.all()
        paginator = LimitOffsetPagination()
        paginator.default_limit = 10

        result_page = paginator.paginate_queryset(recipes, request)
        serializer = RecipeDetailSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class RecipeDetailView(APIView):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)
    
class CuisineStatsView(APIView):
    def get(self, request):
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 10))

        cuisines = Cuisine.objects.annotate(
            recipe_count=Count('recipe'),
            average_rating=Avg('recipe__rating__score')
        )

        total = cuisines.count()

        cuisines = cuisines[offset:offset + limit]

        data = [
            {
                "cuisine_id": str(cuisine.id),
                "cuisine_name": cuisine.name,
                "recipe_count": cuisine.recipe_count,
                "average_rating": round(cuisine.average_rating, 2) if cuisine.average_rating else None
            }
            for cuisine in cuisines
        ]

        return Response({
            "count": total,
            "offset": offset,
            "limit": limit,
            "results": data
        }, status=status.HTTP_200_OK)



class BulkRecipeUploadView(APIView):
    permission_classes = [IsCreator]

    def post(self, request):
        
        excel_file = request.FILES.get('file')
        if not excel_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Save to tmp folder
        tmp_filename = f"media/bulk_uploads/{uuid.uuid4()}.xlsx"
        os.makedirs(os.path.dirname(tmp_filename), exist_ok=True)
        with open(tmp_filename, 'wb+') as destination:
            for chunk in excel_file.chunks():
                destination.write(chunk)


        process_bulk_recipes.delay(tmp_filename, request.user.id)

        return Response({"message": "File uploaded. Processing started."}, status=status.HTTP_202_ACCEPTED)
    
class RecipePDFDownloadView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        recipe_id = request.query_params.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        html = render_to_string("pdf/recipe_card.html", {"recipe": recipe})

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{recipe.title}.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse("PDF generation failed", status=500)

        return response