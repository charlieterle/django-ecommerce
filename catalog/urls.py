from django.urls import path
from django.urls import re_path
from . import views
from django.urls import include

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path(
        "product/<uuid:pk>/",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ),
    path("product/create/", views.ProductCreateView.as_view(), name="product-create"),
    path("product/update/<uuid:pk>/", views.ProductUpdateView.as_view(), name="product-update"),
    path("product/delete/<uuid:pk>/", views.ProductDeleteView.as_view(), name="product-delete"),
    path("signup", views.UserSignupView.as_view(), name="signup"),
]
