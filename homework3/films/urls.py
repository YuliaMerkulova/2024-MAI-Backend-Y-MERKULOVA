from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.api_get, name='api_get'),
    path('films/', views.api_get, name='api_get'),
    path('addfilm/', views.api_post, name='api_post'),
    path('api/put/', views.api_put, name='api_put'),
    path('api/delete/', views.api_delete, name='api_delete'),
]