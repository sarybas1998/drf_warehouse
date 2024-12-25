from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from warehouse_app.models import City, Store, ProductViewCounter, UserProfile, Product, ProductStock, ProductPhoto
from warehouse_app.serializers import CatalogSerializer, ProductDetailSerializer, SearchSerializer, \
    UpdateStocksSerializer


#  set default city and store if not set
def get_or_create_user_profile(user):
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'delivery_address': 'Default Address',
            'city': City.objects.first(),  # Set a default city if it exists
            'store': Store.objects.filter(city=City.objects.first()).first(),
        }
    )
    return profile

class CatalogAPIView(ListAPIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    serializer_class = CatalogSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['product']

    def get_queryset(self):
        user_profile = get_or_create_user_profile(self.request.user)
        store = user_profile.store

        return ProductStock.objects.filter(store=store, quantity__gt=0)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class ProductDetailAPIView(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    serializer_class = ProductDetailSerializer

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        user_profile = get_or_create_user_profile(request.user)
        city = user_profile.city
        store = user_profile.store

        stock = ProductStock.objects.filter(product=product, store=store).first()
        if not stock:
            return Response({"error": "Product not available in the user's city."}, status=404)

        view_counter, created = ProductViewCounter.objects.get_or_create(product=product)
        view_counter.views += 1
        view_counter.save()

        serializer = self.serializer_class(product, context={'request': request, 'city': city, 'store': store})
        return Response(serializer.data)


class SearchAPIView(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    serializer_class = SearchSerializer
    pagination_class = PageNumberPagination

    def get(self, request):
        query = request.GET.get('q', '')
        user_profile = get_or_create_user_profile(request.user)
        city = user_profile.city
        store = user_profile.store

        stocks = ProductStock.objects.filter(
            Q(product__name__icontains=query) | Q(product__description__icontains=query),
            store=store,
            quantity__gt=0
        )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(stocks, request)
        serializer = self.serializer_class(page, many=True, context={'request': request, 'city': city, 'store': store})
        return paginator.get_paginated_response(serializer.data)


class UpdateStocksAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateStocksSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ProductStock.objects.filter(
                product_id=serializer.validated_data['product_id'],
                store_id=serializer.validated_data['store_id']
            ).update(
                quantity=serializer.validated_data['quantity'],
                price=serializer.validated_data['price']
            )
            return Response({"status": "Stocks updated successfully"})
        return Response(serializer.errors, status=400)
