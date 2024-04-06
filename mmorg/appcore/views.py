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
#from .filters import CommentFilter
from django.http import HttpResponseNotFound


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


# class PostsListSearch(ListView):
#     model = Post
#     queryset = Post.objects.filter(type__exact='NE').order_by('-datetime_in')
#     template_name = 'posts_search.html'
#     context_object_name = 'posts_search'
#     paginate_by = 10
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         self.filterset = PostFilter(self.request.GET, queryset)
#         return self.filterset.qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filterset'] = self.filterset
#         return context

class PostsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #u1 = self.request.user
        post_id = self.request.path_info[7:][:-1]
        # u2 = User.objects.get(username=u1)
        #p1 = Post.objects.filter(id = post_id)
        c1 = Comment.objects.filter(post_id=post_id)
        context['Postes'] = c1
        return context


class PostCreate(CreateView):
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


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class FotoList(ListView):
    model = Foto
    #ordering = '-date_create'
    template_name = 'fotos.html'
    context_object_name = 'fotos'
    paginate_by = 10


class CommentCreate(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'
    success_url = ''

class CommentAccept(UpdateView):
    form_class = AcceptCommentForm
    model = Comment
    queryset = Comment.objects.filter(is_ptinjato=False)
    template_name = 'comment_accept.html'
    success_url = '/comments/'

class CommentDelete(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = '/comments/'

    # def get_queryset(self, **kwargs):
    #     #queryset = super().get_queryset()
    #     u1 = self.request.user
    #     p1 = Post.objects.filter(user = u1)
    #     c1 = Comment.objects.select_related('post').filter(post__user=u1)
    #     queryset = c1
    #     #context['Users'] = u1
    #     return queryset

class CommentsList(ListView):
    model = Comment
    ordering = '-date_create'
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = 5
    #CommentFilter
    def get_queryset(self, **kwargs):
        #queryset = super().get_queryset()
        u1 = self.request.user
        p1 = Post.objects.filter(user = u1)
        c1 = Comment.objects.select_related('post').filter(post__user=u1)
        queryset = c1
        #context['Users'] = u1
        return queryset


   # # Переопределяем функцию получения списка товаров
   # def get_queryset(self):
   #     # Получаем обычный запрос
   #     queryset = super().get_queryset()
   #     # Используем наш класс фильтрации.
   #     # self.request.GET содержит объект QueryDict, который мы рассматривали
   #     # в этом юните ранее.
   #     # Сохраняем нашу фильтрацию в объекте класса,
   #     # чтобы потом добавить в контекст и использовать в шаблоне.
   #     self.filterset = ProductFilter(self.request.GET, queryset)
   #     # Возвращаем из функции отфильтрованный список товаров
   #     return self.filterset.qs
   #
   # def get_context_data(self, **kwargs):
   #     context = super().get_context_data(**kwargs)
   #     # Добавляем в контекст объект фильтрации.
   #     context['filterset'] = self.filterset

   # #     return context
   #  def get_queryset(self, **kwargs):
   #      context = super().get_context_data(**kwargs)
   #      u1 = self.request.user
   #      # u2 = User.objects.get(username=u1)
   #      p1 = Post.objects.filter(user = u1)
   #      c1 = Comment.objects.select_related("post").filter(post__user=u1)
   #      context['Commentes'] = c1
   #      #context['Users'] = u1
   #      return context

# def prinjat_otklik(request, pk):
#     user  = request.user
#     comment = Comment.objects.get(id=pk)
#     comment.subscribers.add(user)
#
#     message = 'вы подписались на рассылку новостей категории '
#     return render(request, 'news/subscribe.html', {'category': category, 'message': message})