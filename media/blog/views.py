from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse 
from .models import Post, Comment
from account.models import UserProfile
from .forms import PostForm, PostComment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

# Create your views here.
def index(request):
    blog_posts = Post.objects.all()
    top2=blog_posts.order_by('-last_modified')#[:2]
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
    current_post = Post.objects.get(slug=slug)
    try:
        comments = Comment.objects.filter(post=current_post)  
        #filter returns queryset (can have multiple objects), while get can have 1
    except:
        comments = 'none'
    author_profile = UserProfile.objects.get(user=current_post.author)

    if request.method == "POST":
        create_comment_form = PostComment(request.POST)
        if create_comment_form.is_valid():
            instance = create_comment_form.save(commit=False)
            instance.commenter=request.user
            instance.post=current_post
            instance.save() 
            messages.success(request, "Your commment is created!")  
    create_comment_form = PostComment()
    return render(request, 'blog/posts.html', {
        "posts": current_post,
        "author_profile": author_profile,
        "comments": comments,
        "create_comment_form": create_comment_form
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