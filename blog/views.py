from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse 
from .models import Post
from account.models import UserProfile
from .forms import PostForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

# Create your views here.
def index(request):
    blog_posts = Post.objects.all()
    top2=blog_posts.order_by('-last_modified')[:2]
    return render(request, 'blog/index.html', {
        "posts": top2
    })
    #return HttpResponse('test')

 
def blog_post(request, slug):
    #post_content = {}
    #for post in blog_posts:
    #    if post['slug']==slug:
    #        post_content=post
    #post_content = next(post for post in blog_posts if post['slug']== slug).json()
    blog_posts = Post.objects.all()
    author_profile = UserProfile.objects.get(
        user=blog_posts.get(slug=slug).author
    )
    post_content = blog_posts.get(slug=slug)
    return render(request, 'blog/posts.html', {
        "posts": post_content,
        "author_profile": author_profile
    })

 
def start(request):
    blog_posts = Post.objects.all()
    return render(request, 'blog/start.html', {
        "posts": blog_posts
    })

@login_required(login_url=reverse_lazy('login'))
def new_post(request):
   if request.method == "POST":
       create_post_form = PostForm(request.POST, request.FILES)
       if create_post_form.is_valid():
           instance = create_post_form.save(commit=False)
           instance.author=request.user
           instance.save() 
           messages.success(request, "Your Post is created!")
           return redirect(reverse('posts-page'))
   else:
        create_post_form = PostForm() 
   return render(request, 'blog/create_post.html', {"create_post_form": create_post_form})