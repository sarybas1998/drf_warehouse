from django.urls import reverse
from rest_framework import serializers
from warehouse_app.models import Product, ProductPhoto, ProductStock


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['photo']


class CatalogSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(source="product.id")
    product_name = serializers.CharField(source="product.name")
    city = serializers.CharField(source="store.city.name")
    store_id = serializers.IntegerField(source="store.id")
    store_name = serializers.CharField(source="store.name")
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductStock
        fields = ['product_id', 'product_name', 'price', 'quantity', 'photos', 'city', 'store_id', 'store_name', 'url']

    def get_photos(self, obj):
        request = self.context.get('request')
        photos = ProductPhoto.objects.filter(product=obj.product, city=obj.store.city) or \
                 ProductPhoto.objects.filter(product=obj.product, city__isnull=True)
        return [request.build_absolute_uri(photo.photo.url) for photo in photos]

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('product_detail', args=[obj.product.id]))


class ProductDetailSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    store_id = serializers.SerializerMethodField()
    store_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'photos', 'city', 'store_id', 'store_name', 'price', 'quantity', ]

    def get_price(self, obj):
        store = self.context.get('store')
        stock = ProductStock.objects.filter(product=obj, store=store).first()
        return stock.price if stock else None

    def get_quantity(self, obj):
        store = self.context.get('store')
        stock = ProductStock.objects.filter(product=obj, store=store).first()
        return stock.quantity if stock else None

    def get_photos(self, obj):
        city = self.context.get('city')
        photos = ProductPhoto.objects.filter(product=obj, city=city) or \
                 ProductPhoto.objects.filter(product=obj, city__isnull=True)
        return [photo.photo.url for photo in photos]

    def get_store_id(self, obj):
        store = self.context.get('store')
        return store.id

    def get_store_name(self, obj):
        store = self.context.get('store')
        return store.name

    def get_city(self, obj):
        city = self.context.get('city')
        return city.name


class SearchSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(source="product.id")
    product_name = serializers.CharField(source="product.name")
    city = serializers.CharField(source="store.city.name")
    store_id = serializers.IntegerField(source="store.id")
    store_name = serializers.CharField(source="store.name")
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductStock
        fields = ['product_id', 'product_name', 'price', 'quantity', 'photos', 'city', 'store_id', 'store_name', 'url']

    def get_photos(self, obj):
        city = self.context.get('city')
        photos = ProductPhoto.objects.filter(product=obj.product, city=city) or \
                 ProductPhoto.objects.filter(product=obj.product, city__isnull=True)
        return [photo.photo.url for photo in photos]


    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('product_detail', args=[obj.product.id]))


class UpdateStocksSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    store_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
