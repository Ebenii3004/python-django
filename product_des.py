import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')  # Đổi 'ecommerce' thành tên project bạn nếu khác
django.setup()

from store.models import Product  # Đổi 'store' nếu app của bạn có tên khác

# Danh sách sản phẩm và mô tả tương ứng
descriptions = {
    "LT Sun In Moon VN V4 35": "Thiết kế Sun In Moon độc đáo tượng trưng cho sự hòa hợp giữa mặt trời và mặt trăng, mang đến vẻ đẹp tinh tế và huyền bí.",
    "LT Sun In Moon VN V3 37": "Biểu tượng mặt trời và mặt trăng đan xen, chiếc vòng là sự kết hợp giữa cá tính và nhẹ nhàng.",
    "LT Milky Way Dây Rút 13": "Với họa tiết dải ngân hà, chiếc vòng tạo cảm giác như cả vũ trụ đang ôm trọn cổ tay bạn.",
    "LT Four Leaf Đá Đen SM 27": "Cỏ 4 lá may mắn kết hợp đá đen huyền bí – một phụ kiện sang trọng và cá tính.",
    "LT Four Leaf - Đá Đen 34": "Cỏ 4 lá đính đá đen mang thông điệp may mắn, mạnh mẽ và tinh tế.",
    "LT Cỏ 4 Lá Đá Moonstone 7": "Moonstone sáng lấp lánh kết hợp biểu tượng cỏ 4 lá, mang ý nghĩa bảo vệ và may mắn.",
    "LT Cỏ 4 Lá Tim Đá Hồng 5": "Sự kết hợp giữa biểu tượng may mắn và đá hồng dịu dàng – món quà tuyệt vời cho những trái tim yêu thương.",
    "LT Cỏ 4 Lá Hoa 4 Cánh Hồng": "Thiết kế hoa cánh hồng nhẹ nhàng và nữ tính, làm nổi bật cổ tay người đeo.",
    "LT Cỏ 4 Lá Dây Rút VN 25": "Thiết kế dây rút tiện lợi với biểu tượng cỏ 4 lá mang đến vẻ đẹp năng động và trẻ trung.",
    "LT Cỏ 4 Lá Dây Rút 28": "Phong cách hiện đại kết hợp với sự may mắn truyền thống từ biểu tượng cỏ 4 lá.",
    "LT Blue Sea Circle V4 32": "Cảm hứng từ đại dương xanh, chiếc vòng Blue Sea Circle mang vẻ đẹp tươi mát và sâu lắng.",
    "LTV Vàng Hoa Rơi 46": "Thiết kế hoa rơi tinh tế ánh vàng – sang trọng và nổi bật trong mọi dịp.",
    "DC Nơ Tim Đá Trắng VN 45": "Nơ tim cùng đá trắng sáng lấp lánh, tượng trưng cho sự tinh khiết và tình yêu.",
    "DC Nơ Tim Đá Hồng V9": "Đá hồng và nơ xinh xắn tạo nên điểm nhấn ngọt ngào cho người đeo.",
    "DC Four Leaf - Đá Đen S12": "Cỏ 4 lá đính đá đen – sự lựa chọn hoàn hảo để thu hút may mắn và phong cách.",
    "DC Cỏ 4 Lá V1 - Size S 36": "Cỏ 4 lá đơn giản, tinh tế – biểu tượng của sự may mắn cho mọi ngày.",
    "DC Cỏ 4 Lá Tim Đá CZVN 14": "Tim đá CZ và cỏ 4 lá – nhẹ nhàng và nữ tính nhưng vẫn toát lên nét sang trọng.",
    "DC Cỏ 4 Lá Tim Đá Hồng 8": "Sự kết hợp ngọt ngào giữa cỏ 4 lá và đá hồng – dành cho những trái tim lãng mạn.",
    "DC Cỏ 4 Lá Tim Đá CZVN 7": "Vẻ đẹp thanh lịch với thiết kế tim đá CZ và cỏ 4 lá may mắn.",
    "DC Cỏ 4 Lá Móc VN V2 22": "Móc cài tiện lợi cùng thiết kế cỏ 4 lá tinh xảo – món phụ kiện dễ thương không thể thiếu.",
}

# Cập nhật mô tả sản phẩm
updated = 0
for name, desc in descriptions.items():
    try:
        product = Product.objects.get(name=name)
        product.description = desc
        product.save()
        updated += 1
        print(f"✅ Đã cập nhật: {name}")
    except Product.DoesNotExist:
        print(f"❌ Không tìm thấy sản phẩm: {name}")

print(f"\n🎉 Đã cập nhật {updated}/{len(descriptions)} sản phẩm.")
