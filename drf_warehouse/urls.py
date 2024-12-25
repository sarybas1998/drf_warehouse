# from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/auth/', include('authentication_app.urls')),
    path('api/v1/', include('warehouse_app.urls')),
]
