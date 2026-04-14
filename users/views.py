from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def home(request):
    return render(request, 'base.html')


def profile(request, username):
    user = request.user
    profile_user = get_object_or_404(CustomUser, username=username)

    # Если не авторизован
    if not user.is_authenticated:
        return redirect('login')

    # Если это свой профиль
    if user == profile_user:
        return render(request, 'users/profile.html', {
            'profile_user': profile_user,
            'is_owner': True,
            'is_friend': False,
            'is_mutual': False,
        })

    # Проверяем, являются ли пользователи друзьями (взаимно)
    is_mutual_friend = user.is_friend_with(profile_user)

    # Если мы друзья (взаимно) - показываем полный профиль
    if is_mutual_friend:
        return render(request, 'users/profile.html', {
            'profile_user': profile_user,
            'is_owner': False,
            'is_friend': user.is_friend(profile_user),  # добавил ли я его
            'is_mutual': True,
        })

    # Если не друзья - показываем страницу с кнопкой добавления
    return render(request, 'users/stranger_profile.html', {
        'profile_user': profile_user,
        'is_friend': False,
    })
@login_required
def user_list(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def add_friend(request, username):
    friend = get_object_or_404(CustomUser, username=username)
    request.user.friends.add(friend)
    return redirect('profile', username=username)

@login_required
def remove_friend(request, username):
    friend = get_object_or_404(CustomUser, username=username)
    request.user.friends.remove(friend)
    return redirect('profile', username=username)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.phone = request.POST.get('phone', '')
        user.bio = request.POST.get('bio', '')
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        user.save()
        return redirect('profile', username=user.username)

    return render(request, 'users/edit_profile.html', {'user': request.user})