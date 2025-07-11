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
| Web Server  | Nginx                     |
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


## 📁 Project Structure

├── app/ # Django app with models, views, serializers
├── templates/pdf/ # HTML template for recipe PDF card
├── media/ # Uploaded files (thumbnails, step pictures, Excel files)
├── requirements.txt # Python requirements
├── docker-compose.yml # Docker services: Django, Postgres, Redis, Celery
├── Dockerfile # Python 3.10 slim image
├── README.md # This file



---

## 🚀 API Endpoints

# Base URL - http://3.110.54.154:8000/

### 🔨 Creator
| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/app/recipes/` | Create a recipe |
| `PUT /api/v1/app/recipes/<uuid:pk>/` | Update recipe (partial allowed) |
| `DELETE /api/v1/app/recipes/` | Delete recipe (uses query param `?id=<uuid>`) |
| `POST /api/v1/app/upload-excel/` | Bulk upload recipes via Excel (processed via Celery) |

---

### 👀 Viewer
| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/app/recipes/` | List recipes (offset pagination) |
| `GET /api/v1/app/recipes/<uuid:pk>/` | Recipe detail |
| `POST /api/v1/app/favourites/` | Mark as favourite (query param `?recipe_id=<uuid>`) |
| `DELETE /api/v1/app/favourites/` | Remove from favourites (query param) |
| `POST /api/v1/app/ratings/` | Submit a rating `{ "recipe": <uuid>, "score": 4 }` |
| `GET /api/v1/app/recipe-counts/` | Recipes count & average rating by cuisine |
| `GET /api/v1/app/recipe-pdf/?id=<uuid>` | Download recipe card as PDF |

---

## 📄 Excel Bulk Upload Format

Upload an **`.xlsx` file** with columns:

| title | description | instructions | prep_duration | cook_duration | cuisine_id | ingredient_ids |
|-------|-------------|--------------|---------------|---------------|------------|----------------|
| string | string | string | int | int | uuid | comma-separated uuids |

## ⚙️ Installation

### 🐳 Docker (recommended)
```bash
docker-compose up --build
