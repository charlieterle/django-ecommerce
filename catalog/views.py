from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import CustomUser, Product
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied as Http403


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


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """商品を作成できるビュー"""
    model = Product
    fields = ['name', 'price', 'info']
    permission_required = 'catalog.vendor_status'
    success_url = reverse_lazy('products')
    template_name_suffix = '_create'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.vendor = self.request.user
        self.object.save()
        return super().form_valid(form)


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
    success_message = '会員登録が成功しました。'