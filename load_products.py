import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

from store.models import Product  # Sửa nếu app bạn không phải 'store'

# Đường dẫn đến media/images
MEDIA_IMAGE_DIR = os.path.join('media', 'images')

# Duyệt qua từng file ảnh
for filename in os.listdir(MEDIA_IMAGE_DIR):
    if filename.endswith('.png'):
        # Tên sản phẩm là tên file, bỏ đuôi và thay _ bằng space
        name = os.path.splitext(filename)[0].replace('_', ' ')
        price = random.randint(200, 400) * 1000
        image_path = f'images/{filename}'  # Django lưu image từ 'media/images/...'

        # Tạo sản phẩm
        Product.objects.create(
            name=name,
            price=price,
            image=image_path
        )

print("✅ Tạo sản phẩm thành công từ ảnh trong media/images")
