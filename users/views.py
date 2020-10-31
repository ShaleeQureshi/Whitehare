from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    # form submits as post request
    if request.method == 'POST':
        # creates new form with request data
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Accounted created for {username}, you can now login!")
            return redirect('blog-home')
    else:
        form = UserRegForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_updateform = UserUpdateForm(request.POST, instance=request.user)
        profile_updateform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_updateform.is_valid() and profile_updateform.is_valid():
            user_updateform.save()
            user_updateform.save()
            messages.success(request, f"Successfully updated profile for {user_updateform.cleaned_data.get('username')}")
            # prevents post get redirect pattern, now we only send a get request from browser reload instead of another post request
            return redirect('user-profile')
    else:
        user_updateform = UserUpdateForm(instance=request.user)
        profile_updateform = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_updateform' : user_updateform,
        'profile_updateform' : profile_updateform
    }
    return render(request, 'users/profile.html', context)