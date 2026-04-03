from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/workers', views.WorkerViewSet, basename='worker')
router.register(r'api/tasks', views.DailyTaskViewSet, basename='task')
router.register(r'api/hours', views.WorkHoursViewSet, basename='hour')
router.register(r'api/salaries', views.SalaryViewSet, basename='salary')

urlpatterns = [
    path('', include(router.urls)),
    
    # Specific non-router relations
    path('api/workers/<int:worker_id>/tasks/', views.DailyTaskViewSet.as_view({'get': 'list'})),
    path('api/workers/<int:worker_id>/hours/', views.WorkHoursViewSet.as_view({'get': 'list'})),
    path('api/workers/<int:worker_id>/salary/', views.SalaryViewSet.as_view({'get': 'list'})),

    # Mock Services Routes
    path('mock/lands/', views.mock_lands),
    path('mock/lands/<int:pk>/', views.mock_land_detail),
    path('mock/cultures/', views.mock_cultures),
    path('mock/equipments/', views.mock_equipments),
    path('mock/auth/me/', views.mock_auth_me),
]
