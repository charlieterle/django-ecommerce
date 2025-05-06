from django import forms
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


class MultipleImageField(forms.ImageField):
    """複数の画像をアップロードするフィールド"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_image_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_image_clean(d, initial) for d in data]
        else:
            result = [single_image_clean(data,initial)]
        return result
        

class MultipleFileInput(forms.ClearableFileInput):
    """複数ファイルアップロードを可能にするインプット"""
    allow_multiple_selected = True


class ProductCreateForm(forms.ModelForm):
    """商品作成フォーム"""
    images = MultipleImageField(widget = MultipleFileInput(attrs={
            "name": "images",
            "type": "File",
            "multiple": "True",
        }),
        required=False,
        label='商品画像',
    )
    class Meta:
        model = Product
        fields = ['name', 'price', 'info']
