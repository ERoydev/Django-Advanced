import asyncio
from datetime import datetime

from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import classonlymethod
from django.views.generic import ListView, CreateView, FormView

from .forms import PostBaseForm, SearchForm, PostCommentForm, PostEditForm, PostCreateForm, PostConfirmForm
from .models import Post, Comment
from django.views import generic as views, View


UserModel = get_user_model()

# class BaseView:
#     # Nachina po koito raboti
#     @classonlymethod
#     def as_view(cls):
#         def view(request, *args, **kwargs):
#             view_instance = cls()
#             return view_instance.dispatch(request, *args, **kwargs)
#
#         return view
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.method == "GET":
#             return self.get(request, *args, **kwargs)
#
#         elif request.method == "POST":
#             return self.post(request, *args, **kwargs)

# Show Posts(CBV) and (FBV) ---------------
# Class Based View

# class ShowPosts(views.TemplateView):
#     template_name = 'posts.html' # Static Way
#
#     def get_context_data(self, **kwargs):
#         # First, get the default context from the parent class
#         context = super().get_context_data(**kwargs)
#
#         context['all_posts'] = Post.objects.all()
#         return context

# Function Base View
# def show_posts(request):
#     all_posts = Post.objects.all()
#
#     context = {
#         "all_posts": all_posts
#     }
#
#     return render(request, 'posts.html', context)
# END OF Show Posts -----------------------

class DashboardView(ListView, FormView):
    template_name = 'posts.html'
    form_class = SearchForm
    success_url = reverse_lazy('show_posts')
    context_object_name = 'posts'
    model = Post
    paginate_by = 2
    extra_context = {
        'static_time': datetime.now()
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['dynamic_time'] = datetime.now(),

        return context


    def get_queryset(self): # I take the query from the form
        queryset = self.model.objects.all()

        if 'posts.can_approve_posts' not in self.request.user.get_group_permissions() or not self.request.user.has_perm('posts.can_approve_posts'):
            queryset = queryset.filter(approved=True)

        if 'query' in self.request.GET:
            query = self.request.GET.get('query')
            queryset = queryset.filter(title__icontains=query)

        return queryset


# Add Post (CBV) and (FBV)
# Class Based View
class AddPost(LoginRequiredMixin, views.CreateView):
    model = Post
    form_class = PostBaseForm
    template_name = 'add_form.html'
    success_url = reverse_lazy('show_posts')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # I set programmatically the user instead of in frontend form
        form.instance.author = self.request.user

        # Save the post instance using the parent's form_valid
        response = super().form_valid(form)

        # Best approach in synchronous func like this View is to use sync_to_async() approach
        async_to_sync(notify_all_users)(self.object.pk)

        # Because create_task requires event loop which i don't have in synchronous func like that
        # I cannot use .run() either it creates loop but it block everything until the task is completed in order to create and close this loop
        # asyncio.create_task(notify_all_users(self.object.pk))

        return response


# Function Based View
def add_post(request):
    form = PostBaseForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        "form": form
    }

    return render(request, 'add_form.html', context)

# Details (CBV) and (FBV)
# Class Based Views

class DetailPostView(views.DetailView):
    model = Post
    template_name = 'post-details.html'
    # context_object_name = 'post' // in built in the context_name is set to model name
    form_class = PostCommentForm

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = PostCommentForm(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                instance = form.save(commit=False)
                instance.post = post
                instance.save()
                return redirect('details_post', pk=post.pk)

            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        current_object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['all_comments'] = Comment.objects.filter(post=current_object.pk)
        return context


# Function Based View
def details(request, pk):
    post = Post.objects.get(pk=pk)
    all_comments = Comment.objects.filter(post=pk)
    commentForm = PostCommentForm(request.POST or None)

    if request.method == "POST":
        if commentForm.is_valid():
            cleaned_data = commentForm.cleaned_data
            cleaned_data['post'] = post

            Comment.objects.create(**cleaned_data)

    context = {
        "post": post,
        "commentForm": commentForm,
        "all_comments": all_comments
    }

    return render(request, 'post-details.html', context)


class EditPostView(views.UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'edit-post.html'
    success_url = reverse_lazy('show_posts')

    def get_form_class(self):
        if self.request.user.is_superuser:
            return modelform_factory(Post, fields=('title', 'content', 'author', 'languages'))
        else:
            return modelform_factory(Post, fields=('content',))


def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostEditForm(request.POST or None, instance=post)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('show_posts')

    context = {
        "form": form,
        "post": post
    }

    return render(request, 'edit-post.html', context)


class DeletePostView(views.DeleteView):
    model = Post
    success_url = reverse_lazy('show_posts')


def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('show_posts')


def search(request):
    form = SearchForm(request.GET)

    context = {
        "form": form
    }

    return render(request, 'search.html', context)


class ApprovePostView(View):
    def post(self, request, pk):
        # Get the post and update approval status
        post = get_object_or_404(Post, pk=pk)
        post.approved = True
        post.save()

        # Redirect to success URL
        return redirect(reverse_lazy('show_posts'))

    def get(self, request, pk):
        # Render the confirmation page for GET requests
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'approve-post.html', {'post': post})


async def fetch_post_and_users(post_id):
    post = await Post.objects.select_related('author').aget(pk=post_id) # Join
    all_users = await sync_to_async(UserModel.objects.exclude)(id=post.author.id)
    all_users_to_list = await sync_to_async(list)(all_users)
    return post, all_users_to_list


async def send_slow_email(subject, message, origin, to):
    await sync_to_async(send_mail)(
        subject=subject,
        message=message,
        from_email=origin,
        recipient_list=[to]
    )


async def notify_all_users(post_id):
    # post = Post.objects.aget(pk=post_id) Async Get
    post, all_users = await fetch_post_and_users(post_id)

    subject = f'New Post: {post.title}'
    message = f'{post.author.username} wrote:\n\n{post.content}'

    email_tasks = [
        send_slow_email(
            subject,
            message,
            'no-reply@forumapp.com',
            user.email
        ) # Does not call the function it returns an object
        for user in all_users
    ]

    await asyncio.gather(*email_tasks)

    return HttpResponse("Done")
