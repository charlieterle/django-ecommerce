import os
import django
import urllib.request
import json
from urllib.error import HTTPError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommercesite.settings')
django.setup()

from catalog.models import CustomUser, Product, Image
from django.contrib.auth.hashers import make_password

# 既存のダミーデータを削除 
Product.objects.all().delete()
Image.objects.all().delete()
CustomUser.objects.filter(username__in=["alice", "bob", "carol"]).delete()

# 空ディレクトリを削除
for dirpath, dirnames, filenames in os.walk(django.conf.settings.MEDIA_ROOT, topdown=False):
    if not dirnames and not filenames:
        try:
            os.removedirs(dirpath)
            print(f"空ディレクトリを削除しました: {dirpath}")
        except Exception as e:
            print(f"{dirpath} の削除に失敗しました: {e}")


# ユーザーを作成
users_data = [
    {"username": "alice", "email": "alice@example.com", "password": "testpass123", "family_name": "山田"},
    {"username": "bob", "email": "bob@example.com", "password": "testpass123", "family_name": "佐藤"},
    {"username": "carol", "email": "carol@example.com", "password": "testpass123", "family_name": "鈴木"},
]
users = []
for u in users_data:
    user, created = CustomUser.objects.get_or_create(username=u["username"], defaults={
        "email": u["email"],
        "password": make_password(u["password"]),
        "family_name": u["family_name"]
    })
    users.append(user)

# 商品データをJSONから読み込み
with open('products_data.json', encoding='utf-8') as f:
    products_data = json.load(f)

demo_dir = os.path.join(django.conf.settings.MEDIA_ROOT, 'images', 'demo')
os.makedirs(demo_dir, exist_ok=True)

for i, pdata in enumerate(products_data):
    vendor = users[i % len(users)]
    product = Product.objects.create(
        name=pdata["name"],
        info=pdata["info"],
        price=pdata["price"],
        vendor=vendor,
    )
    # 画像ダウンロード
    img_filename = f"demo_product_{i+1}.jpg"
    img_path = os.path.join(demo_dir, img_filename)
    try:
        urllib.request.urlretrieve(pdata["image_url"], img_path)
        with open(img_path, 'rb') as f:
            image = Image(product=product)
            image.image.save(img_filename, django.core.files.File(f), save=True)
    except HTTPError as e:
        if e.code == 404:
            print(f"画像が見つかりませんでした (404): {product.name}。この商品は削除されます。")
            product.delete()
        else:
            raise

print("デモデータの投入が完了しました。")

# demoディレクトリを削除
for fname in os.listdir(demo_dir):
    fpath = os.path.join(demo_dir, fname)
    try:
        os.remove(fpath)
    except Exception as e:
        print(f"{fpath} の削除に失敗しました: {e}")
os.rmdir(demo_dir)