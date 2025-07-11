# 🚀 Recipe Management System




A Django REST Framework based API for managing recipes, built as part of a technical assessment.

## ✍️ Features

- **Two types of users**: 
  - 🔨 Creator: Can create, list, modify, delete recipes. Can upload recipes in bulk using an Excel file.
  - 👀 Viewer: Can view list & detail of recipes, mark recipes as favourites, download recipe cards as PDF.
- 📊 Viewers can see:
  - Recipe count per cuisine
  - Average rating of recipes per cuisine
- ⭐ Rating system: Viewers can rate recipes from 1-5.
- 📦 Each recipe includes:
  - Title, description, instructions
  - Prep & cook duration
  - Thumbnail image & step-by-step pictures
  - Ingredients with name & picture

---

## 🛠️ Tech Stack

| Layer       | Technology                |
|-------------|---------------------------|
| Backend     | Django (Python)           |
| Database    | PostgreSQL                |
| Caching     | Redis                     |
| Task Queue  | Celery                    |
| Deployment  | Docker, AWS (EC2)    |


## 🚀 Postman Collection

You can use the provided Postman collection to test the entire API.

- [📥 Download Postman Collection](https://github.com/PrabhatTheCoder/receipe-management/blob/fc852d453e80966b6973752e5628546370716c54/Receipe%20Management.postman_collection.json)

### 🔥 How to use
1. Open Postman > Import > Upload `recipe-management-collection.json`.
2. Set the environment variables for:
   - `{{base_url}}` = `http://localhost:8000/api/v1/app`
   - `{{access_token}}` (optional if using authenticated endpoints)
3. Run your requests.

✅ Contains examples for:
- Creating recipes
- Bulk upload with Excel
- Marking favourites
- Downloading recipe PDF
- Getting counts & ratings

## 📂 Project Structure

```plaintext
recipe-management/
│
├── app/                  # Django app for recipes, cuisines, ingredients, ratings, favourites
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         # All core models: Recipe, Cuisine, Ingredient, etc.
│   ├── serializers.py    # DRF serializers
│   ├── permissions.py    # Custom permissions (IsCreator, IsViewer, etc.)
│   ├── views.py          # API views
│   ├── urls.py           # API routes for this app
│   └── tests.py
│
├── users/                # Custom user model with user_type (creator / viewer)
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── media/                # Uploaded media files (thumbnails, step pictures, ingredient images)
│
├── recipe_management/    # Main Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py           # Includes app + users urls
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

```


---

## 🚀 API Endpoints

# Base URL - http://3.110.54.154:8000/

### 🔨 Creator
| Method | Endpoint                                | Description                                 |
| ------ | --------------------------------------- | ------------------------------------------- |
| POST   | `/api/v1/app/create-receipe/`           | Create a new recipe                         |
| PUT    | `/api/v1/app/update-receipe/<uuid:pk>/` | Update an existing recipe (partial allowed) |
| DELETE | `/api/v1/app/delete-receipe/?id=<uuid>` | Delete a recipe using query param `id`      |
| POST   | `/api/v1/app/create-ingredients/`       | Create ingredients                          |
| POST   | `/api/v1/app/create-cuisine/`           | Create cuisine                              |
| POST   | `/api/v1/app/create-step-picture/`      | Upload step pictures                        |


---

### 👀 Viewer
| Method | Endpoint                               | Description                                   |
| ------ | -------------------------------------- | --------------------------------------------- |
| GET    | `/api/v1/app/list-recipes/`            | List all recipes (supports pagination)        |
| GET    | `/api/v1/app/detail-recipe/<uuid:pk>/` | Get detailed info of a recipe                 |
| GET    | `/api/v1/app/recipe-pdf/?id=<uuid>`    | Download recipe card as PDF                   |
| GET    | `/api/v1/app/cuisine-stats/`           | Get recipe count & average ratings by cuisine |



### ⭐ Favourites & Ratings
| Method | Endpoint                                          | Description                                        |
| ------ | ------------------------------------------------- | -------------------------------------------------- |
| POST   | `/api/v1/app/create-favourites/?recipe_id=<uuid>` | Mark a recipe as favourite                         |
| DELETE | `/api/v1/app/create-favourites/?recipe_id=<uuid>` | Remove recipe from favourites                      |
| POST   | `/api/v1/app/create-ratings/`                     | Submit a rating `{ "recipe": <uuid>, "score": 4 }` |

---

### ⭐ Users

| Method | Endpoint                  | Description                            |
| ------ | ------------------------- | -------------------------------------- |
| POST   | `/auth/register-user/`    | Register a new user (creator / viewer) |
| POST   | `/auth/login/`            | Login & get access + refresh tokens    |
| POST   | `/auth/logout/`           | Logout (invalidate refresh token)      |
| POST   | `/auth/get-access-token/` | Get new access token using refresh     |


### 📄 Excel Bulk Upload

| Method | Endpoint                    | Description                                           |
| ------ | --------------------------- | ----------------------------------------------------- |
| POST   | `/api/v1/app/upload-excel/` | Upload Excel file to bulk create recipes (via Celery) |

POST	/api/v1/app/upload-excel/	Upload Excel file to bulk create recipes (processed via Celery)

## 📄 Excel Bulk Upload Format

Upload an **`.xlsx` file** with columns:

You can use this sample Excel sheet to test the **bulk upload API** for recipes.

👉 **[Download sample_recipes.xlsx](https://github.com/PrabhatTheCoder/receipe-management/blob/main/Receipe_Excel.xlsx)**

| title          | description    | instructions       | prep_duration | cook_duration | cuisine_id                          | ingredient_ids                                     |
|----------------|----------------|--------------------|---------------|---------------|-------------------------------------|----------------------------------------------------|
| Test Recipe 1  | Yummy Dish 1   | Do not cook.       | 20            | 10            | 6368a720-51f1-49ce-9a39-3cdddc1a79f6 | ["e66cf8f0-d825-4ff0-bf79-41ff54db3863"]           |
| Test Recipe 2  | Yummy Dish 2   | Just watch.        | 30            | 15            | 6368a720-51f1-49ce-9a39-3cdddc1a79f6 | ["a1bf6758-6fa7-4011-849c-5a411d7eceb4"]           |


## ⚙️ Installation

### 🐳 Docker (recommended)
```bash
docker-compose up --build
