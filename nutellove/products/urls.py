from django.urls import path

from . import views  # import views so we can use them in urls.
from .models import Favorite, Brand, Category

# required for django 2.0
app_name = "products"

urlpatterns = [
    # what to display for url products/
    path('', views.listing),
    # what to display for url products/<id>
    path(
        '<int:product_id>',
        views.ProductDetail.as_view(),
        name='product_detail',
    ),
    # what to display for url products/search/?query=<query>
    path(
        'search/', views.Search.as_view(),
        name='search',
    ),
    # use a custom link to boorkmark products
    path(
        'bookmark/<int:product_id>',
        views.FavoriteView.as_view(model=Favorite),
        name="bookmark",
    ),
    # favorites/
    path(
        'favorites/',
        views.FavoriteView.as_view(model=Favorite),
        name="favorites",
    ),
    # brands/
    path(
        'brands/',
        views.BrandCategoryDetail.as_view(
            model=Brand,
        ),
        name="brands"
    ),
    # brands/<int:brand_id>
    path(
        'brands/<int:obj_id>',
        views.BrandCategoryDetail.as_view(
            model=Brand,
        ),
        name="brand_detail",
    ),
    path(
        'categories/',
        views.BrandCategoryDetail.as_view(
            model=Category,
        ),
        name="categories",
    ),
    # categories/<int:category_id>
    path(
        'categories/<int:obj_id>',
        views.BrandCategoryDetail.as_view(
            model=Category,
        ),
        name="category_detail",
    ),
]
