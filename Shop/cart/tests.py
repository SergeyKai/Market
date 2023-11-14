from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Cart, CartItem
from products.models import ProductVariant, Product, Category, Supplier, Color
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

User = get_user_model()


class CartTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        supplier = Supplier.objects.create(title='Test Supplier', address='Test Address')
        category = Category.objects.create(title='Test Category', image='category/test_image.jpg')
        color = Color.objects.create(title='Test Color', code='#ffffff')
        product = Product.objects.create(title='Test Product', supplier=supplier, description='Test Description',
                                         category=category)
        product_variant = ProductVariant.objects.create(price=100, product=product, color=color, quantity=10,
                                                        availability=True, attributes={'size': 'medium'})

        self.cart = Cart.objects.create(user=user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=product_variant, quantity=2)

    def test_cart_total_price(self):
        total_price = self.cart.get_total()
        self.assertEqual(total_price, 200)

    def test_cart_item_quantity(self):
        item_quantity = self.cart_item.quantity
        self.assertEqual(item_quantity, 2)


class UserShoppingTest(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome(executable_path='path/to/chromedriver')
        super(UserShoppingTest, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(UserShoppingTest, self).tearDown()

    def test_user_shopping_flow(self):
        # Шаг 1: Авторизация пользователя
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('testuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('testpassword')
        password_input.send_keys(Keys.RETURN)

        # Шаг 2: Добавление товара в корзину
        self.selenium.get('%s%s' % (self.live_server_url, '/shop/products/1/'))
        add_to_cart_button = self.selenium.find_element_by_id("add-to-cart-button")
        add_to_cart_button.click()

        # Шаг 3: Проверка общей стоимости заказа в корзине
        cart_total_price = self.selenium.find_element_by_id("cart-total-price").text
        self.assertEqual(cart_total_price, '200 ₽')

        # Шаг 4: Оформление заказа
        checkout_button = self.selenium.find_element_by_id("checkout-button")
        checkout_button.click()

        # Шаг 5: Проверка наличия заказа в истории пользователя
        order_history_button = self.selenium.find_element_by_id("order-history-button")
        order_history_button.click()
        order_count = len(self.selenium.find_elements_by_class_name("order-item"))
        self.assertEqual(order_count, 1)
