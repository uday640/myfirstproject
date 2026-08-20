from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("profile")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("profile")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form": form})


@login_required(login_url='login')
def profile_view(request):
    context = {
        'user': request.user,
        'user_id': request.user.id,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        # USERNAME UPDATE
        user.username = request.POST.get('username')

        # PASSWORD CHANGE (OPTIONAL)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password:
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('edit_profile')
            user.set_password(password)
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Account updated successfully.")
        return redirect('profile')

    return render(request, 'edit_profile.html')


def logout_view(request):
    logout(request)
    return redirect('login')