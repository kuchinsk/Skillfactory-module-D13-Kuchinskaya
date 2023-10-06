from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin, UpdateView

from .filters import PostFilter
from .models import Post, Response
from .forms import PostForm, ResponseForm


class Board(ListView):
    model = Post
    template_name = 'board.html'
    context_object_name = 'board'
    queryset = Post.objects.order_by('-timePost')
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        # context['filter_author'] = AuthorFilter(self.request.GET, queryset=self.get_queryset())
        # context['filter_category'] = CategoryFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostView(LoginRequiredMixin, DetailView, FormMixin):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post_detail'
    queryset = Post.objects.all()

    form_class = ResponseForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = form.save(commit=False)
        response.responseUser = self.request.user
        response.responsePost = Post.objects.get(id=self.kwargs['pk'])
        author_post = Post.objects.get(id=self.kwargs['pk'])
        user_post = author_post.author
        user_email = user_post.email
        response.save()
        subject = 'Пользователь оставил отклик на ваше объявление'
        message = f'Пользователь {response.responseUser.username} оставил ответ на ваш отклик.'
        from_email = 'kuchinsk93@yandex.ru'
        recipient_list = [user_email]

        send_mail(subject, message, from_email, recipient_list)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('board:post', args=[self.kwargs['pk']])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.filter(responsePost=self.object)
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = 'post.add_Post'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.instance.author = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # return reverse('board', kwargs={'pk': self.object.pk})
        return reverse('board:post_create')


class PostUpdate (LoginRequiredMixin, UpdateView):
    template_name = 'post_update.html'
    form_class = PostForm
    permission_required = 'post.change_post'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)