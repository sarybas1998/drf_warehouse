from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from warehouse_app.models import City, Store, Product, ProductStock, UserProfile

from decimal import Decimal

class CatalogAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create city and store
        self.city = City.objects.create(name='Test City')
        self.store = Store.objects.create(name='Test Store', city=self.city)

        # Create product and stock
        self.product = Product.objects.create(name='Test Product', description='Test Description', default_price=100.00)
        self.stock = ProductStock.objects.create(product=self.product, store=self.store, price=120.00, quantity=5)

        # Create user profile
        UserProfile.objects.create(user=self.user, delivery_address='123 Test St', city=self.city, store=self.store)

    def test_get_catalog(self):
        response = self.client.get('/api/v1/catalog/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['product_name'], 'Test Product')
        self.assertEqual(response.data['results'][0]['city'], 'Test City')

    def test_catalog_no_city(self):
        profile = self.user.user_profile
        profile.city = None
        profile.store = None
        profile.save()
        response = self.client.get('/api/v1/catalog/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.data['results'])

class ProductDetailAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create city and store
        self.city = City.objects.create(name='Test City')
        self.store = Store.objects.create(name='Test Store', city=self.city)

        # Create product and stock
        self.product = Product.objects.create(name='Test Product', description='Test Description', default_price=100.00)
        self.stock = ProductStock.objects.create(product=self.product, store=self.store, price=120.00, quantity=5)

        # Create user profile
        UserProfile.objects.create(user=self.user, delivery_address='123 Test St', city=self.city, store=self.store)

    def test_product_detail(self):
        response = self.client.get(f'/api/v1/product/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')
        self.assertEqual(response.data['price'], Decimal('120.00'))

    def test_product_detail_not_in_city(self):
        other_city = City.objects.create(name='Other City')
        other_store = Store.objects.create(name='Other Store', city=other_city)
        profile = self.user.user_profile
        profile.city = other_city
        profile.store = other_store
        profile.save()
        response = self.client.get(f'/api/v1/product/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SearchAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create city and store
        self.city = City.objects.create(name='Test City')
        self.store = Store.objects.create(name='Test Store', city=self.city)

        # Create products and stock
        self.product1 = Product.objects.create(name='Test Product 1', description='Description 1', default_price=100.00)
        self.product2 = Product.objects.create(name='Another Product', description='Description 2', default_price=150.00)
        ProductStock.objects.create(product=self.product1, store=self.store, price=120.00, quantity=10)
        ProductStock.objects.create(product=self.product2, store=self.store, price=140.00, quantity=5)

        # Create user profile
        UserProfile.objects.create(user=self.user, delivery_address='123 Test St', city=self.city, store=self.store)

    def test_search(self):
        response = self.client.get('/api/v1/search/?q=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['product_name'], 'Test Product 1')

class UpdateStocksAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create city and store
        self.city = City.objects.create(name='Test City')
        self.store = Store.objects.create(name='Test Store', city=self.city)

        # Create product and stock
        self.product = Product.objects.create(name='Test Product', description='Test Description', default_price=100.00)
        self.stock = ProductStock.objects.create(product=self.product, store=self.store, price=120.00, quantity=5)

    def test_update_stock(self):
        data = {'product_id': self.product.id, 'store_id': self.store.id, 'quantity': 15, 'price': 110.00}
        response = self.client.post('/api/v1/catalog/update/stocks', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 15)
        self.assertEqual(self.stock.price, 110.00)
