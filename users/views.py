import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm
from .models import CustomUser

# Создаём логгер для модуля
logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        logger.info(f"User {username} logged in successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        username = form.cleaned_data.get('username', 'unknown')
        logger.warning(f"Failed login attempt for username: {username}")
        return super().form_invalid(form)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        logger.info(f"User registered successfully: {self.object.username} (email: {self.object.email})")
        return response

    def form_invalid(self, form):
        logger.warning(f"Registration failed - validation errors: {form.errors.as_json()}")
        return super().form_invalid(form)


def home(request):
    return render(request, 'base.html')


def profile(request, username):
    user = request.user
    profile_user = get_object_or_404(CustomUser, username=username)

    if not user.is_authenticated:
        logger.warning(f"Unauthenticated user tried to view profile: {username}")
        return redirect('login')

    # Если это свой профиль
    if user == profile_user:
        logger.info(f"User {user.username} viewed their own profile")
        return render(request, 'users/profile.html', {
            'profile_user': profile_user,
            'is_owner': True,
        })

    # Если это профиль друга
    if profile_user in user.friends.all():
        logger.info(f"User {user.username} viewed friend's profile: {username}")
        return render(request, 'users/profile.html', {
            'profile_user': profile_user,
            'is_owner': False,
            'is_friend': True,
        })

    # Если это профиль не-друга
    logger.info(f"User {user.username} viewed stranger's profile: {username}")
    return render(request, 'users/stranger_profile.html', {
        'profile_user': profile_user,
    })


@login_required
def user_list(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    logger.info(f"User {request.user.username} viewed user list")
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def add_friend(request, username):
    friend = get_object_or_404(CustomUser, username=username)
    request.user.friends.add(friend)
    logger.info(f"User {request.user.username} added {username} as friend")
    return redirect('profile', username=username)


@login_required
def remove_friend(request, username):
    friend = get_object_or_404(CustomUser, username=username)
    request.user.friends.remove(friend)
    logger.info(f"User {request.user.username} removed {username} from friends")
    return redirect('profile', username=username)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.phone = request.POST.get('phone', '')
        user.bio = request.POST.get('bio', '')

        # Обработка аватарки с логированием ошибок
        if request.FILES.get('avatar'):
            try:
                user.avatar = request.FILES['avatar']
                # Проверка типа файла
                if not user.avatar.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    raise ValidationError("File is not an image")
                logger.info(f"User {user.username} uploaded new avatar: {user.avatar.name}")
            except Exception as e:
                logger.error(f"User {user.username} failed to upload avatar: {str(e)}", exc_info=True)
                return render(request, 'users/edit_profile.html', {
                    'user': user,
                    'error': 'Invalid file format. Please upload an image (PNG, JPG, GIF).'
                })

        user.save()
        logger.info(f"User {user.username} updated profile")
        return redirect('profile', username=user.username)

    return render(request, 'users/edit_profile.html', {'user': request.user})