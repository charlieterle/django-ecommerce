from django.shortcuts import render
from django.views import generic
from .models import Product
from django.shortcuts import render, get_object_or_404


def index(request):
    return render(request, "index.html")


class ProductListView(generic.ListView):
    """商品のリストを表すビュー"""

    model = Product
    paginate_by = 25


class ProductDetailView(generic.DetailView):
    """商品の詳細を表すビュー"""

    model = Product
