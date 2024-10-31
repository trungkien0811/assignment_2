from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from selenium.webdriver.support.wait import WebDriverWait

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.saucedemo.com")
    yield driver
    driver.quit()


#TC1: Kiểm tra đăng nhập thành công
def test_valid_login(driver):
    #Nhập thông tin đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    #Nhấn login
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)
    current_url = driver.current_url
    # Kiểm tra URL hiện tại
    assert current_url == "https://www.saucedemo.com/inventory.html", f"Expected URL: 'https://www.saucedemo.com/inventory.html', but got: '{current_url}'"

#TC2: Kiểm tra đăng nhập thất bại
def test_invalid_login(driver):
    # Nhập thông tin đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("free_fire_max")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)
    #Chờ thông báo error xuất hiện
    error_message_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
    )
    # Lấy nội dung thông báo
    error_message_text = error_message_element.text
    print(error_message_text)
    assert error_message_text == "Epic sadface: Username and password do not match any user in this service"

#TC3: Kiểm tra đăng nhập với tài khoản và mật khẩu trống.
def test_empty_login(driver):
    # Nhập thông tin đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("")
    driver.find_element(By.ID, "password").send_keys("")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)
    #Chờ thông báo error xuất hiện
    error_message_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
    )
    # Lấy nội dung thông báo
    error_message_text = error_message_element.text
    print(error_message_text)
    assert error_message_text == "Epic sadface: Username is required"

#TC4: Kiểm tra log out
def test_log_out(driver):
    #Đăng nhập thành công
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)
    #Bấm nút menu
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    #Đợi nút log out xuất hiện
    button_log_out = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "logout_sidebar_link"))
    )
    button_log_out.click()
    time.sleep(3)
    #url có phải trang chủ?
    current_url = driver.current_url
    # Kiểm tra URL hiện tại
    assert current_url == "https://www.saucedemo.com/"

#TC5: Kiểm tra add to cart
def test_add_to_cart(driver):
    #Đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)
    #Thêm 1 sản phẩm vào giỏ
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(2)
    #kiểm tra thêm thành công chưa bằng trạng thái nút từ add -> remove
    button_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@id='remove-sauce-labs-backpack']"))
    )
    # Lấy nội dung của thẻ button
    button_text = button_element.text
    assert button_text == "Remove"

#TC6: Kiểm tra truy cập vào giỏ hàng
def test_acess_to_cart(driver):
    #Đăng nhập
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    #Bấm vào nút giỏ hàng
    driver.find_element(By.CLASS_NAME, "shopping_cart_container").click()
    time.sleep(2)
    # url có phải trang giỏ hàng?
    current_url = driver.current_url
    # Kiểm tra URL hiện tại
    assert current_url == "https://www.saucedemo.com/cart.html"


#TC7: Kiểm tra xoá 1 sản phẩm khỏi giỏ hàng
def test_remove_one_item_to_cart(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    #Thêm 1 sản phẩm vào giỏ trước để đảm bảo giỏ có sản phẩm
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(2)
    #Id nút đổi, tức đã thêm vào giỏ thành công
    button_element1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@id='remove-sauce-labs-backpack']"))
    )
    #Bấm vào nút giỏ hàng
    driver.find_element(By.CLASS_NAME, "shopping_cart_container").click()
    time.sleep(2)
    #Xoá sản phẩm vừa thêm
    button_element2 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "remove-sauce-labs-backpack"))
    )
    button_element2.click()
    time.sleep(2)
    a = 0
    #Kiểm tra xem thẻ chứa sản phẩm vừa xoá khỏi giỏ có còn không
    try:
        cart_item_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cart_item"))
        )
        a = 1
    except Exception:
        a = 0
    assert a == 0


#TC8: Kiểm tra truy cập trang thanh toán
def test_check_out(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    #Thêm vào 1 sản phẩm
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(2)
    button_element1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@id='remove-sauce-labs-backpack']"))
    )
    driver.find_element(By.CLASS_NAME, "shopping_cart_container").click()
    time.sleep(2)
    driver.find_element(By.ID, "checkout").click()
    time.sleep(2)
    url = driver.current_url
    assert url == "https://www.saucedemo.com/checkout-step-one.html"

#TC9: Kiểm tra truy cập trang thanh toán khi giỏ hàng trống
def test_check_out_with_no_item(driver):
    #Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    #Truy cập giỏ hàng
    driver.find_element(By.CLASS_NAME, "shopping_cart_container").click()
    time.sleep(2)
    #Truy cập thanh toán
    driver.find_element(By.ID, "checkout").click()
    time.sleep(2)
    #Nếu chuyển hướng đến trang thanh toán -> fails
    url = driver.current_url
    assert url == "https://www.saucedemo.com/cart.html", print(url)

#TC10: Kiểm tra bỏ trống nội dung thanh toán
def test_check_empty_check_out(driver):
    #Thực hiện giống TC8
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(2)
    button_element1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@id='remove-sauce-labs-backpack']"))
    )
    driver.find_element(By.CLASS_NAME, "shopping_cart_container").click()
    time.sleep(2)
    #Nhấn nút để mở trang thanh toán
    driver.find_element(By.ID, "checkout").click()
    time.sleep(2)
    #Nhấn nút để hoàn tất thanh toán mà không điền nội dung
    driver.find_element(By.ID, "continue").click()
    #Chờ thông báo lỗi
    error_message_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
    )
    # Lấy nội dung thông báo
    error_message_text = error_message_element.text
    print(error_message_text)
    assert error_message_text == "Error: First Name is required"

#TC11: Kiểm tra đường dẫn trên trang có khả dụng
def test_link(driver):
    # Mở trang web
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
    )
    unique_hrefs = set(link.get_attribute("href") for link in links)
    # In ra danh sách các href khác nhau
    for href in unique_hrefs:
        print(href)
    #tạo list link chứa link hỏng
    list_link = []
    for url in unique_hrefs:
        if url is None or url == "":
            #Đường dẫn rỗng
            continue
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code >= 400:
                #Đường dẫn lỗi sẽ được thêm vào list
                list_link.append(url)
            else:
                #Những url sai
                pass
        except requests.exceptions.RequestException as e:
            print(f"Error checking {url}: {e}")
    #nếu list rỗng thì pass
    assert not list_link, print(list_link)

#TC12: Kiểm tra hiển thị của trang trên nhiều màn hình
def test_layout(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    #Danh sách màn hình
    screen_sizes = {
        "s1": (1920, 800),
        "s2": (720, 1020),
        "s3": (375, 667),
        "s4": (325, 500)
    }
    #List chứa màn hình lôi
    List = []
    for device, (width, height) in screen_sizes.items():
        # Thay đổi kích thước cửa sổ
        driver.set_window_size(width, height)
        # Kiểm tra các yếu tố trên trang
        try:
            # Chờ cho một phần tử quan trọng cụ thể xuất hiện (header_label)
            header = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "header_label"))
            )
            if not header.is_displayed():
                #Không hiển thị thì thêm màn hình vừa test vào list
                List.append(device)
        except Exception as e:
            #lỗi thêm vào list
            List.append(device)
    #List rỗng trả về pass
    assert not List, print(List)

#TC13: Kiểm tra filter giá tăng dần
def test_sort(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    # Chờ cho tất cả các thẻ có class 'inventory_item_price' xuất hiện
    price_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_price"))
    )
    # Lấy giá trị chữ số sau ký hiệu $ và lưu vào danh sách
    prices = []
    for element in price_elements:
        price_text = element.text
        # Lấy giá trị số sau ký hiệu $
        if price_text.startswith("$"):
            price_value = price_text[1:]  # Bỏ ký hiệu $
            prices.append(float(price_value))  # Chuyển đổi thành float và thêm vào danh sách
    # In ra danh sách giá
    print("\nstart")
    print(prices)
    #tìm select box filter
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))
    )
    # Tạo đối tượng Select
    select = Select(select_element)
    # Chọn giá trị số 2 (tức là "Price (low to high)")
    select.select_by_value("lohi")  # Hoặc có thể dùng select.select_by_index(2)
    time.sleep(3)
    price_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_price"))
    )
    #Giá sau khi bấm filter
    prices2 = []
    for element in price_elements:
        price_text = element.text
        # Lấy giá trị số sau ký hiệu $
        if price_text.startswith("$"):
            price_value = price_text[1:]  # Bỏ ký hiệu $
            prices2.append(float(price_value))  # Chuyển đổi thành float và thêm vào danh sách
    print("\nafter filter")
    print(prices)
    #Nếu danh sách giá gốc sau khi sort bằng với danh sách giá sau filter thì pass
    assert sorted(prices) == prices2


