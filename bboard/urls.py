from django.urls import path
from .views import index, about, add_bb, read_bb, update_bb, delete_bb

app_name = 'bboard'
urlpatterns = [
    path('', index, name='index'),
    path('bb/<int:pk>/delete/', delete_bb, name="delete_bb"),
    path('bb/<int:pk>/edit/', update_bb, name='update_bb'),
    path('bb/<int:pk>/', read_bb, name="read_bb"),
    path('bb/', add_bb, name='add_bb'),
    path('about/', about, name='about')
]