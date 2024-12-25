from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    class Meta:
        db_table = 'warehouse_city'

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, related_name='store', db_index=True)

    class Meta:
        db_table = 'warehouse_store'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True, db_index=True)
    default_price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

    class Meta:
        db_table = 'warehouse_product'

    def __str__(self):
        return self.name


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name='product_photo', db_index=True)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, null=True, blank=True, related_name='product_photo',
                             db_index=True)
    photo = models.ImageField(upload_to='product_photos/')

    class Meta:
        db_table = 'warehouse_product_photo'

    def __str__(self):
        return self.product.name


class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name='product_stock', db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT, related_name='product_stock', db_index=True)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'warehouse_product_stock'

    def __str__(self):
        return self.product.name


class ProductViewCounter(models.Model):
    product = models.OneToOneField(Product, on_delete=models.RESTRICT, related_name='view_counter', db_index=True)
    views = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        db_table = 'warehouse_product_view_counter'

    def __str__(self):
        return self.product.name


class UserProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name='user_profile')
    delivery_address = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, null=True)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT, null=True)

    class Meta:
        db_table = 'warehouse_product_user_profile'

    def __str__(self):
        return self.user.username
