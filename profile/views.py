import datetime
from urllib import request
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, FormView
from urllib3.util import request

from .filters import ResponseFilter
from .forms import SignForm, LoginForm, CodeForm
from django.core.mail import send_mail
import random

from board.models import Post, Response
from .models import TimeCode


class ProfileView(ListView):
    model = Post
    template_name = 'profile/profile.html'
    context_object_name = 'author_posts'
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        obj = Post.objects.filter(author=self.request.user).order_by('-timePost')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.user
        context['email'] = self.request.user.email

        return context


class ResponseView(ListView):
    model = Response
    template_name = 'profile/response.html'
    context_object_name = 'responses'
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        responses_user = Response.objects.filter(responsePost__author=user)
        user_responses_to_other_ads = Response.objects.filter(responseUser=user)

        combined_responses = user_responses_to_other_ads | responses_user
        combined_responses = combined_responses.order_by('-textResponse')

        return combined_responses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ResponseFilter(self.request.GET, queryset=self.get_queryset())
        context['not_accept'] = Response.objects.filter(acceptResponse=False)
        return context


def accept(request, pk):
    Response.objects.filter(pk=pk).update(acceptResponse=True)

    subject = 'Ваш отклик принят автором'
    message = f'Автор принял ваш отклик {Response.objects.get(pk=pk).textResponse}'
    from_email = 'kuchinsk93@yandex.ru'
    recipient_list = [Response.objects.get(pk=pk).responseUser.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return redirect('/profile/response')


def delete(request, pk):
    Response.objects.get(pk=pk).delete()
    return redirect('/profile/response')


class SignView(CreateView):
    model = User
    form_class = SignForm
    template_name = 'sign/signup.html'
    success_url = '/profile/code'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = SignForm(request.POST)
            if form.is_valid():
                user = form.save()
                code = user.id
                TimeCode.objects.create(code=code, user=user)
                request.session['user'] = f'{user}'
                user_email = form.cleaned_data['email']
                subject = 'Одноразовый код для регистрации'
                message = f'Ваш одноразовый код для регистрации: {code}'
                from_email = 'kuchinsk93@yandex.ru'  # Укажите вашу почту здесь
                recipient_list = [user_email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                group = Group.objects.get_or_create(name='basic')[0]
                user.groups.add(group)
                user.save()
                return super().form_valid(form)


class CodeView(FormView):
    form_class = CodeForm
    template_name = 'sign/code.html'
    success_url = '/login'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.session.get('user', 0)
            code = TimeCode.objects.get(user__username=username).code
            form = CodeForm(request.POST)
            if form.is_valid():
                code_w = form.cleaned_data["verified_fieid"]
                if code_w == code:
                    # user = authenticate(self.request, username=username, password=password)
                    # group = Group.objects.get_or_create(name='basic')[0]
                    # self.request.user.groups.add(group)
                    # self.request.user.save()
                    return redirect('/profile/login')
                else:
                    return render(request, 'sign/signup.html')
        else:
            form = CodeView()
        return render(request, 'sign/code.html', {'form': form})


class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'sign/login.html'
    success_url = '/profile'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')
