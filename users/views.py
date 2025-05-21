from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users import forms
from django.utils.translation import gettext_lazy as _
from django import forms

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Mật khẩu')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Xác nhận mật khẩu')
    full_name = forms.CharField(max_length=100, label='Họ và tên')
    birthdate = forms.DateField(label='Ngày sinh', widget=forms.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(max_length=15, label='Số điện thoại')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError(_('Mật khẩu và xác nhận mật khẩu không khớp.'))

        if User.objects.filter(username=cleaned_data.get('username')).exists():
            raise ValidationError(_('Tên đăng nhập đã tồn tại.'))

        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError(_('Email đã được sử dụng.'))

        return cleaned_data

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, "Đăng nhập thành công!")
                return redirect('/')  # Chuyển hướng đến trang chủ
        messages.error(request, "Thông tin đăng nhập không hợp lệ.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()
            messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
            return redirect('login')  # Thay 'login' bằng tên URL đăng nhập
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

from datetime import datetime

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('users:profile')

    # Fake danh sách đơn hàng mẫu
    orders = [
        {'code': 'DH001', 'date': datetime(2025, 4, 20), 'status': 'Đã giao', 'total': 150000},
        {'code': 'DH002', 'date': datetime(2025, 4, 22), 'status': 'Đang xử lý', 'total': 200000},
        {'code': 'DH003', 'date': datetime(2025, 4, 25), 'status': 'Đã hủy', 'total': 0},
    ]

    return render(request, 'users/profile.html', {'orders': orders})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {
        'user': request.user
    })
    

