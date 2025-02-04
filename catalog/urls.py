from django.urls import path
from django.urls import re_path
from . import views
from django.urls import include

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path(
        "product/<uuid:pk>",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ),
    path("signup/", views.UserSignupView.as_view(), name="signup")
]
