from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.forms import CustomPasswordResetForm
from users.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Кастомный вход с логированием
    path('auth/login/', CustomLoginView.as_view(), name='login'),

    # Кастомные URL для восстановления пароля (с нашей формой)
    path('auth/password_reset/',
         auth_views.PasswordResetView.as_view(
             form_class=CustomPasswordResetForm,
             template_name='registration/password_reset_form.html'
         ),
         name='password_reset'),

    path('auth/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('auth/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('auth/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # Стандартные URL авторизации (кроме login, который мы заменили)
    path('auth/', include('django.contrib.auth.urls')),

    # URL нашего приложения
    path('', include('users.urls')),
]

# Для загрузки аватарок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)