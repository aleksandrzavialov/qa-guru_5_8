"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    # TODO напишите проверки на метод check_quantity
    def test_product_check_quantity_positive_non_zero_equal(self, product):
        assert product.check_quantity(1000)

    def test_product_check_quantity_positive_non_zero_non_equal(self, product):
        assert product.check_quantity(530)

    def test_product_check_quantity_positive_zero(self):
        zero_product = Product('mars', 50.0, 'Chocolate', 0)
        assert zero_product.check_quantity(0)

    def test_product_check_quantity_negative_non_zero(self, product):
        assert not product.check_quantity(1001)

    def test_product_check_quantity_negative_zero(self):
        test_zero_product = Product('meat', 750.87, 'Pork', 0)
        assert not test_zero_product.check_quantity(1)

    def test_product_check_quantity_negative_less_than_zero(self, product):
        with pytest.raises(Exception) as exc_info:
            product.check_quantity(-1)
        assert str(exc_info.value) == 'Please enter value >=0'

    # TODO напишите проверки на метод buy
    def test_product_buy_left_more_than_zero(self, product):
        product.buy(25)
        assert product.quantity == 975

    def test_product_buy_left_zero(self, product):
        product.buy(1000)
        assert product.quantity == 0

    def test_product_buy_negative_quantity(self, product):
        with pytest.raises(Exception) as exc_info:
            product.buy(-900)
        assert str(exc_info.value) == 'You can buy only positive amount'

    def test_product_buy_zero_quantity(self, product):
        with pytest.raises(Exception) as exc_info:
            product.buy(0)
        assert str(exc_info.value) == 'You can buy only positive amount'

    # TODO напишите проверки на метод buy,
    #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
    def test_product_buy_more_than_available_non_zero_exist(self, product):
        with pytest.raises(Exception) as exc_info:
            product.buy(1001)
        assert str(exc_info.value) == f'Not enough items in storage for {product.name}'

    def test_product_buy_more_than_available_zero_exist(self):
        with pytest.raises(Exception) as exc_info:
            buy_quantity = 2
            test_zero_product = Product('lamb', 1800.0, 'Young lamb', 0)
            test_zero_product.buy(buy_quantity)
        assert str(exc_info.value) == f'Not enough items in storage for {test_zero_product.name}'


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    # test add_product() function
    def test_cart_add_one_product_in_empty_cart_with_default_quantity(self, cart, product):
        cart.add_product(product)
        assert cart.products[product] == 1

    def test_cart_add_one_product_in_cart_with_another_product(self, cart, product):
        existing_product = Product('vodka', 570.00, 'Rasputin', 3)
        cart.add_product(existing_product, 2)
        cart.add_product(product, 7)
        assert cart.products[existing_product] == 2
        assert cart.products[product] == 7

    def test_cart_add_one_product_in_cart_with_same_product(self, cart, product):
        cart.add_product(product, 20)
        cart.add_product(product, 7)
        assert cart.products[product] == 27

    # test remove_product() function
    def test_cart_remove_product_cart_pass_count_so_amount_is_zero(self, cart, product):
        cart.add_product(product, 2)
        cart.remove_product(product, 2)
        assert cart.products[product] == 0

    def test_cart_remove_product_cart_pass_count_so_one_item_remains(self, cart, product):
        cart.add_product(product, 2)
        cart.remove_product(product, 1)
        assert cart.products[product] == 1

    def test_cart_remove_product_cart_pass_count_so_product_is_deleted(self, cart, product):
        cart.add_product(product, 3)
        cart.remove_product(product, 4)
        assert product.name not in cart.products.keys()

    def test_cart_remove_product_cart_default_count_so_product_is_deleted(self, cart, product):
        cart.add_product(product, 1)
        cart.remove_product(product)
        assert product.name not in cart.products.keys()

    def test_cart_remove_absent_product_in_cart(self, cart, product):
        with pytest.raises(Exception) as exc_info:
            cart.remove_product(product)
        assert str(exc_info.value) == f'You cannot delete {product} because it is not in the cart'

    # test clear() function
    def test_cart_clear_non_empty_cart_three_products(self, cart, product):
        tested_product_pork = Product('meat', 750.87, 'Pork', 3)
        tested_product_bacon = Product('meat', 750.87, 'Bacon', 2)
        cart.add_product(product, 1)
        cart.add_product(tested_product_pork, 1)
        cart.add_product(tested_product_bacon, 2)
        cart.clear()
        assert len(cart.products) == 0

    def test_cart_clear_empty_cart(self, cart):
        cart.clear()
        assert len(cart.products) == 0

    # test get_total_price
    def test_get_total_price_two_products(self, cart, product):
        product_cheese = Product('cheese', 1800.43, 'Mozarella', 8)
        cart.add_product(product, 33)
        cart.add_product(product_cheese, 5)
        assert cart.get_total_price() == 3300 + 9002.15

    def test_get_total_price_two_products_one_was_removed(self, cart, product):
        product_cheese = Product('cheese', 1800.43, 'Mozarella', 8)
        product_honey = Product('honey', 5500.86, 'Tasty', 4)
        cart.add_product(product, 33)
        cart.add_product(product_cheese, 5)
        cart.add_product(product_honey, 4)
        cart.remove_product(product_cheese)
        assert cart.get_total_price() == 3300 + 5500.86 * 4

    def test_get_total_price_empty_cart(self, cart):
        assert cart.get_total_price() == 0

    # test buy
    def test_buy_two_different_products(self, cart, product):
        product_honey = Product('honey', 2340.89, 'Tasty', 40)
        cart.add_product(product, 30)
        cart.add_product(product_honey, 1)
        assert cart.buy() == 30 * 100 + 2340.89 * 1
        assert len(cart.products) == 0

    def test_buy_same_product_added_twice(self, cart, product):
        cart.add_product(product, 30)
        cart.add_product(product, 11)
        assert cart.buy() == (30 + 11) * 100
        assert len(cart.products) == 0

    def test_buy_three_products_two_removed(self, cart, product):
        tested_product_pork = Product('meat', 750.87, 'Pork', 38)
        tested_product_bacon = Product('meat', 750.87, 'Bacon', 2)
        cart.add_product(product, 1)
        cart.add_product(tested_product_pork, 10)
        cart.add_product(tested_product_bacon, 2)
        cart.remove_product(product)
        cart.remove_product(tested_product_pork)
        assert cart.buy() == 2 * 750.87
        assert len(cart.products) == 0

    def test_buy_empty_cart(self, cart):
        assert cart.buy() == 0
        assert len(cart.products) == 0

    def test_buy_clear_non_empty_cart(self, cart, product):
        tested_product_beer = Product('beer', 75.00, 'Bacon', 200)
        cart.add_product(product, 1)
        cart.add_product(tested_product_beer, 199)
        cart.clear()
        assert cart.buy() == 0
        assert len(cart.products) == 0
