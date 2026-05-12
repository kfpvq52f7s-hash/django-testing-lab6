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

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        logger.info(f"[AUTH] User '{username}' has signed in")
        return super().form_valid(form)

    def form_invalid(self, form):
        username = form.cleaned_data.get('username', 'unknown')
        logger.warning(f"[AUTH] Invalid credentials for user: {username}")
        return super().form_invalid(form)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        logger.info(f"[REGISTER] New account created: {self.object.username} ({self.object.email})")
        return response

    def form_invalid(self, form):
        logger.warning(f"[REGISTER] Validation failed: {form.errors.as_json()}")
        return super().form_invalid(form)


def home(request):
    return render(request, 'base.html')


def profile(request, username):
    user = request.user
    profile_user = get_object_or_404(CustomUser, username=username)

    if not user.is_authenticated:
        logger.warning(f"[PROFILE] Guest attempted to access profile: {username}")
        return redirect('login')

    if user == profile_user:
        logger.info(f"[PROFILE] {user.username} opened own page")
        return render(request, 'users/profile.html', {
            'profile_user': profile_user,
            'is_owner': True,
        })

    if profile_user in user.friends.all():
        logger.info(f"[PROFILE] {user.username} visited friend: {username}")
        return render(request, 'users/profile.html', {
            'profile_user': profile_user,
            'is_owner': False,
            'is_friend': True,
        })

    logger.info(f"[PROFILE] {user.username} visited user: {username}")
    return render(request, 'users/stranger_profile.html', {
        'profile_user': profile_user,
    })


@login_required
def user_list(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    logger.info(f"[USERS] {request.user.username} browsed the user directory")
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def add_friend(request, username):
    friend = get_object_or_404(CustomUser, username=username)
    request.user.friends.add(friend)
    logger.info(f"[FRIENDS] {request.user.username} added {username}")
    return redirect('profile', username=username)


@login_required
def remove_friend(request, username):
    friend = get_object_or_404(CustomUser, username=username)
    request.user.friends.remove(friend)
    logger.info(f"[FRIENDS] {request.user.username} unfriended {username}")
    return redirect('profile', username=username)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.phone = request.POST.get('phone', '')
        user.bio = request.POST.get('bio', '')

        if request.FILES.get('avatar'):
            try:
                user.avatar = request.FILES['avatar']
                if not user.avatar.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    raise ValidationError("File is not an image")
                logger.info(f"[PROFILE] {user.username} changed avatar: {user.avatar.name}")
            except Exception as e:
                logger.error(f"[PROFILE] Avatar upload error for {user.username}: {str(e)}", exc_info=True)
                return render(request, 'users/edit_profile.html', {
                    'user': user,
                    'error': 'Invalid file format. Please upload an image (PNG, JPG, GIF).'
                })

        user.save()
        logger.info(f"[PROFILE] {user.username} updated their information")
        return redirect('profile', username=user.username)

    return render(request, 'users/edit_profile.html', {'user': request.user})
