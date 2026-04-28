from django.contrib import admin
from django.urls import path, include
from services.worker_service.workers.views import index_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    # Map everything to our workers app urls without a prefix here
    # Since our workers/urls.py defines internal api/ and mock/ prefixes
    path('', include('services.worker_service.workers.urls')),
]
