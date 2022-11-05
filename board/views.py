from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Post, Response, Category
from .forms import AddPostForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives


class PostsList(ListView):
    model = Post
    template_name = 'board/main.html'
    context_object_name = 'posts'
    ordering = ['-creation_time']
    paginate_by = 2


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'board/add_post.html'
    form_class = AddPostForm
    success_url = '/main/'

    def form_valid(self, form):
        files = self.request.FILES.getlist('files')

        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.attached_files = [f.name for f in files]
        instance.save()

        for f in files:
            _handle_uploaded_file(f)

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'board/edit.html'
    form_class = AddPostForm
    success_url = '/main/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDetail(DetailView):
    model = Post
    template_name = 'board/post.html'
    context_object_name = 'post'


def _handle_uploaded_file(f):
    ''' Запись в файл "покусочно" '''
    with open(f'media/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='/accounts/login/')
def make_response(request, post_pk):
    text = request.POST['response_text']
    post = Post.objects.get(pk=post_pk)
    if text:
        Response.objects.create(text=text, post=post, sender=request.user)
        html_content = render_to_string(
            'email_templates/response_given.html', {'post': post, 'sender': request.user, 'author': post.author}
        )
        msg = EmailMultiAlternatives(
            subject='Новый отклик',
            body=f'Здравствуй, {post.author.username}. Твой отклик приняли!',
            from_email=None,
            to=[post.author.email, ],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return redirect('/main/')


@login_required(login_url='/accounts/login/')
def personal_posts_view(request, username):
    categories = Category.objects.all()
    if request.GET:
        posts_by_title = Post.objects.filter(author=request.user, title__icontains=request.GET['search'])
        posts_by_text = Post.objects.filter(author=request.user, text__icontains=request.GET['search'])
        posts_by_cat = Post.objects.filter(author=request.user, category__category_name__icontains=request.GET['categories'])
        if posts_by_cat or request.GET['categories']:
            posts = (posts_by_title | posts_by_text)
            posts = posts.filter(category__category_name__icontains=request.GET['categories'])
        else:
            posts = posts_by_title | posts_by_text
    else:
        posts = Post.objects.filter(author=request.user)
    context = {
        'posts': posts.order_by('-creation_time'),
        'categories': categories,
    }
    return render(request, 'board/personal_posts.html', context)


@login_required(login_url='/accounts/login/')
def personal_responses_view(request, username):
    responses = Response.objects.none()
    if request.GET:
        author_posts = Post.objects.filter(author=request.user, title__icontains=request.GET['search'])
    else:
        author_posts = Post.objects.filter(author=request.user)

    for post in author_posts:
        responses = responses | Response.objects.filter(post=post)

    context = {
        'responses': responses.order_by('-creation_time'),
    }

    return render(request, 'board/personal_responses.html', context)


@login_required(login_url='/accounts/login/')
def delete_post(request, pk):
    if pk:
        Post.objects.get(pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/accounts/login/')
def delete_response(request, pk):
    if pk:
        Response.objects.get(pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/accounts/login/')
def accept_response(request, pk):
    if pk:
        response = Response.objects.get(pk=pk)
        response.is_confirmed = True
        response.save()

        html_content = render_to_string(
            'email_templates/response_accepted.html', {'post': response.post, 'user': response.sender}
        )
        msg = EmailMultiAlternatives(
            subject= 'Ответ на отклик',
            body=f'Здравствуй, {response.sender.username}. Твой отклик приняли!',
            from_email=None,
            to=[response.sender.email, ],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return redirect(request.META.get('HTTP_REFERER'))


