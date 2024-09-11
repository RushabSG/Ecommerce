from django.urls import path
from . import views

urlpatterns = [
    # store main page
    path("", views.store, name="store"),
    # individual product
    path("product/<slug:slug>", views.product_info, name="product_info"),
    # Induvidual Category
    path("category/<slug:slug>", views.list_category, name="list_category"),
]
