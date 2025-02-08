from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Product

class CustomUserCreationForm(UserCreationForm):
    """ユーザー登録のフォーム"""
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'family_name', 'given_name',)

class CustomUserChangeForm(UserChangeForm):
    """ユーザー変更フォーム"""
    class Meta(UserChangeForm.Meta):
        model = CustomUser

#class ProductUploadForm(ModelForm):
#    """商品を作成できるフォーム"""
#    class Meta:
#        model = Product
#        fields = ['name', 'price', 'info']