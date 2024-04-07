from django.shortcuts import render
import hashlib
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from appcore.models import OneTimeCode, Post, Comment, Foto, Video, File, PostFoto, PostVideo, PostFile
from .forms import MyActivationCodeForm, PostForm, CommentForm
from django.contrib.auth import authenticate, login
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
#from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm, AcceptCommentForm
from django.db.models import Q
from .filters import CommentFilter
from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import F
from django.contrib.auth.mixins import UserPassesTestMixin



def get_hash_md5(self,filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def activation(request):
    if request.user.is_authenticated:
        return redirect('/posts/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get('code')
                print('code_use',code_use)
                if OneTimeCode.objects.filter(code=code_use):
                    code1 = OneTimeCode.objects.get(code=code_use)
                    p1 = EmailAddress.objects.get(user_id=code1.user.id)
                else:
                    form.add_error(None, 'Неправильный код')
                    return render(request, 'account/email/activate.html', {'form': form})
                if not p1.verified:
                    p1.verified = True
                    p1.save()

                    u1 = User.objects.get(id = p1.user_id)
                    user = authenticate(request, username=u1.username, password=u1.password)
                    if user is not None:
                        login(request, user)

                    code1.delete()
                    return redirect('/accounts/login/')
                else:
                    form.add_error(None, 'Unknown or disabled account')
                return render(request, 'account/email/activate.html', {'form': form})
            else:
                form.add_error(None, 'Форма не валидна')
                return render(request, 'account/email/activate.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'account/email/activate.html', {'form': form})


class PostsList(ListView):
    model = Post
    ordering = '-date_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.request.path_info[7:][:-1]
        c1 = Comment.objects.filter(post_id=post_id)
        context['Postes'] = c1
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = ''

    def form_valid(self, form):
        post = form.save(commit=False)
        author = User.objects.filter(username = self.request.user).values('id')
        author_id = author.values_list('id')[0][0]
        post.user_id = author_id
        post.save()
        fotos = self.request.FILES.getlist('foto')
        if fotos:
            for foto in fotos:
                foto_obj = Foto(image = foto)
                foto_obj.save()
                post_foto_obj = PostFoto(post=post, foto=foto_obj)
                post_foto_obj.save()

        videos = self.request.FILES.getlist('video')
        if videos:
            for video in videos:
                video_obj = Video(video=video)
                video_obj.save()
                post_video_obj = PostVideo(post=post, video=video_obj)
                post_video_obj.save()

        files = self.request.FILES.getlist('file')
        if files:
            for file in files:
                file_obj = File(file=file)
                file_obj.save()
                post_file_obj = PostFile(post=post, file=file_obj)
                post_file_obj.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def test_func(self):
        news = self.get_object()
        return news.user == self.request.user


class PostDelete(LoginRequiredMixin,UserPassesTestMixin,  DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def test_func(self):
        news = self.get_object()
        return news.user == self.request.user


class FotoList(LoginRequiredMixin, ListView):
    model = Foto
    template_name = 'fotos.html'
    context_object_name = 'fotos'
    paginate_by = 10


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'
    success_url = ''

class CommentAccept(LoginRequiredMixin, UpdateView):
    form_class = AcceptCommentForm
    model = Comment
    queryset = Comment.objects.filter(is_ptinjato=False)
    template_name = 'comment_accept.html'
    success_url = '/comments/'


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = '/comments/'


class CommentsList(LoginRequiredMixin, ListView):
    model = Comment
    ordering = '-date_create'
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = 5

    def get_queryset(self):
        #queryset = super().get_queryset()
        u1 = self.request.user
        c1 = Comment.objects.select_related('post').filter(post__user=u1)
        queryset = c1
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u1 = self.request.user
        print('self.request.user',self.request.user)
        c1 = Comment.objects.select_related('post').filter(post__user=u1)
        queryset = c1
        #self.filterset = CommentFilter(self.request.GET, queryset)
        #print('self.filterset',self.filterset.qs)
        context['filterset'] = self.filterset
        return context

