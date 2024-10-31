
Website kiểm thử: https://www.saucedemo.com
Ngôn ngữ lập trình: Python
Brower: Chrome, FireFox
IDE: PyCharm
Thư viện sử dụng: pytest, time, request, selenium
Driver: được cài tự động khi pip install thư viện selenium.
---------------------------
Danh sách Chức năng và test case.

Chức năng: Đăng nhập

TC1: Kiểm tra đăng nhập thành công 
passed in 14.16s
TC2: Kiểm tra đăng nhập thất bại
passed in 12.35s
TC3: Kiểm tra đăng nhập với tài khoản và mật khẩu trống.
passed in 12.21s

Chức năng: Đăng xuất

TC4: Kiểm tra log out
passed in 16.95s

Chức năng: Thêm vào giỏ hàng

TC5: Kiểm tra add to cart
passed in 14.66s

Chức năng: Giỏ hàng

TC6: Kiểm tra truy cập vào giỏ hàng
passed in 13.52s
TC7: Kiểm tra xoá 1 sản phẩm khỏi giỏ hàng
passed in 28.63s

Chức năng: Thanh toán

TC8: Kiểm tra truy cập trang thanh toán
passed in 15.40s
TC9: Kiểm tra truy cập trang thanh toán khi giỏ hàng trống
failed in 11.40s
TC10: Kiểm tra bỏ trống nội dung thanh toán
passed in 17.90s

Chức năng: Đường dẫn

TC11: Kiểm tra đường dẫn trên trang có khả dụng
failed in 9.44s

Chức năng: Phản ứng của bố cục

TC12: Kiểm tra hiển thị của trang trên nhiều màn hình
passed in 12.91s

Chức năng: Tìm tiếm

TC13: Kiểm tra filter giá tăng dần.
passed in 14.50s

----------------------------------
Báo cáo lỗi

TC9: Lỗi không chặn mở trang check out
assert url == "https://www.saucedemo.com/cart.html", print(url)
E       AssertionError: None
E       assert 'https://www.saucedemo.com/checkout-step-one.html' == 'https://www.saucedemo.com/cart.html'

TC11: Lỗi trả về các đường dẫn không khả dụng
assert not list_link, print(list_link)
E       AssertionError: None
E       assert not ['https://www.saucedemo.com/inventory.html#', 'https://www.linkedin.com/company/sauce-labs/', 'https://twitter.com/saucelabs']

