from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import CustomUser, Product, Image
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProductCreateForm, MultipleImageField
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied as Http403
from .filters import ProductFilter


def index(request):
    """ホームページのビュー"""
    return render(request, 'index.html')


class ProductListView(ListView):
    """商品のリストを表すビュー"""
    model = Product
    paginate_by = 25


class ProductDetailView(DetailView):
    """商品の詳細を表すビュー"""
    model = Product

def product_create_view(request):
    """商品を作成できるビュー"""
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            images = request.FILES.getlist('images')
            for image in images:
                image_ins = Image(image=image, product=product)
                image_ins.save()
            return HttpResponseRedirect(product.get_absolute_url())
    else:
        form = ProductCreateForm()
    return render(request, 'catalog/product_create.html', {'form': form}) 

def product_image_upload_view(request, pk=None):
    """画像をアップロードできるビュー"""
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = MultipleImageField(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images')
            for image in images:
                image_ins = Image(image=image, product=product)
                image_ins.save()
            return HttpResponseRedirect(product.get_absolute_url())
    else:
        form = MultipleImageField()
    return render(request, 'catalog/product_image_upload.html', {'form': form})

# TODO Permissionをこのビュー（あるいは他の関数のビュー）に追加
def product_images_update_view(request, pk=None):
    """商品の写真を表すビュー。ここから写真の追加ビューと削除ビューに行けます。"""
    product = Product.objects.get(id=pk)
    return render(request, 'catalog/product_images_update.html', {'product': product}) 
   
def image_delete_view(request, pk=None):
    """画像を削除するビュー"""
    image = Image.objects.get(id=pk)
    if request.method == 'POST':
        if request.user != image.product.vendor:
            raise Http403
        product = image.product
        image.delete()
        return HttpResponseRedirect(product.get_absolute_url())
    return render(request, 'catalog/image_delete.html', {'image': image})

class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    """商品を編集するビュー"""
    model = Product
    permission_required = 'catalog.vendor_status'
    fields = ['name', 'price', 'status', 'info']
    success_url = reverse_lazy('products')
    template_name_suffix = '_update'
    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        # ログイン中のユーザーが商品の売り手でない場合は403エラーを返す
        if obj.vendor != self.request.user:
            raise Http403 
        return obj


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    """商品を削除するビュー"""
    model = Product
    permission_required = 'catalog.vendor_status'
    success_url = reverse_lazy('products')
    template_name_suffix = '_delete'
    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        # ログイン中のユーザーが商品の売り手でない場合は403エラーを返す
        if obj.vendor != self.request.user:
            raise Http403 
        return obj


class UserSignupView(SuccessMessageMixin, CreateView):
    """ユーザーが登録できるビュー"""
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    success_message = '会員登録が成功しました。ログインしてください。'
