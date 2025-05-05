from django.urls import path
from django.urls import re_path
from . import views
from django.urls import include
from django_filters.views import FilterView
from .filters import ProductFilter
from .models import Product
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<uuid:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/", FilterView.as_view(model=Product, filterset_class=ProductFilter), name="products"),
    path("product/create/", views.product_create_view, name="product-create"),
    path("product/<uuid:pk>/update", views.ProductUpdateView.as_view(), name="product-update"),
    path("product/<uuid:pk>/delete", views.ProductDeleteView.as_view(), name="product-delete"),
    path("signup", views.UserSignupView.as_view(), name="signup"),
    path("product/<uuid:pk>/images", views.product_images_view, name="product-images"),
    path("images/<int:imagepk>/delete", views.product_image_delete_view, name="product-image-delete"),
]