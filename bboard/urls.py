from django.urls import path
from django.views.generic import TemplateView

from .views import index, about, add_bb, read_bb, update_bb, delete_bb, user_bbs, user_info, search_bb, filter_bb

app_name = 'bboard'
urlpatterns = [
    path('filter/', filter_bb, name="filter_bb"),
    path('search/', search_bb, name='search_bb'),
    path('', index, name='index'),
    path('bb/<int:pk>/delete/', delete_bb, name="delete_bb"),
    path('bb/<int:pk>/edit/', update_bb, name='update_bb'),
    path('bb/<int:pk>/', read_bb, name="read_bb"),
    path('bb/', add_bb, name='add_bb'),
    path('about/', about, name='about'),
    path('bb/user/info/<int:user_id>/', user_info, name='user_info'),
    path('bb/user/<int:user_id>/', user_bbs, name='user_bbs'),
    path('403/', TemplateView.as_view(template_name='bboard/403.html')),
    path('404/', TemplateView.as_view(template_name='bboard/404.html')),
    path('500/', TemplateView.as_view(template_name='bboard/500.html')),
]