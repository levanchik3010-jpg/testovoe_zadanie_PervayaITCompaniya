from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:record_id>/', views.edit_record, name='edit_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('api/categories/', views.get_categories, name='api-categories'),
    path('api/subcategories/', views.get_subcategories, name='api-subcategories'),
]