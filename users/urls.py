from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.home, name='home'),
    path('users/', views.user_list, name='user_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/add/', views.add_friend, name='add_friend'),
    path('profile/<str:username>/remove/', views.remove_friend, name='remove_friend'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]

# Для загрузки аватарок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)