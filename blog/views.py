from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
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
    current_post = Post.objects.get(slug=slug)
    try:
        comments = Comment.objects.filter(post=current_post)  
        #filter returns queryset (can have multiple objects), while get can have 1
    except:
        comments = 'none'
    author_profile = UserProfile.objects.get(user=current_post.author)

    if request.method == "POST" and "submit_comment" in request.POST:
        create_comment_form = PostComment(request.POST)
        if create_comment_form.is_valid():
            instance = create_comment_form.save(commit=False)
            instance.commenter=request.user
            instance.post=current_post
            instance.save() 
            messages.success(request, "Your commment is created!")
            return HttpResponseRedirect(reverse("post-detail-page", kwargs={'slug':slug}))
    #Attend and unattend button
    if request.method == "POST" and "attend_button" in request.POST:
        current_post.attending.add(request.user)
        messages.success(request, "You are attending the event!")
        return HttpResponseRedirect(reverse("post-detail-page", kwargs={'slug':slug}))
    if request.method == "POST" and "unattend_button" in request.POST:
        current_post.attending.remove(request.user)
        messages.success(request, "You have removed yourself from the event!")
        return HttpResponseRedirect(reverse("post-detail-page", kwargs={'slug':slug}))
    create_comment_form = PostComment() 
    #Like/Unlike post button
    if request.method == "POST" and "like_post" in request.POST:
        if request.user.is_authenticated:
            if request.user in current_post.likes.all():
                current_post.likes.remove(request.user)
            else:
                current_post.likes.add(request.user)
        else:
            messages.info(request, "You need to login to like post")
        return HttpResponseRedirect(reverse("post-detail-page", kwargs={'slug':slug}))
    #Like/Unlike comment button
    if request.method == "POST" and "like_comment" in request.POST:
        comment_id = request.POST.get("like_comment")
        current_comment = current_post.comment_set.get(id=comment_id)
        if request.user.is_authenticated:
            if request.user in current_comment.likes.all():
                current_comment.likes.remove(request.user)
            else:
                current_comment.likes.add(request.user) 
        else:
            messages.info(request, "You need to login to like comments")
        return HttpResponseRedirect(reverse("post-detail-page", kwargs={'slug':slug}))
    print(author_profile)
    return render(request, 'blog/posts.html', {
        "posts": current_post,
        "author_profile": author_profile,
        "comments": comments,
        "create_comment_form": create_comment_form, 
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

@login_required(login_url=reverse_lazy('login'))
def edit_post(request, id):
    current_post = Post.objects.get(id=id)
    if request.user != current_post.author:
        messages.info(request, "Your cannot edit post as you are not the author!")
        return redirect(reverse('posts-page'))
    if request.method == "POST":
       edit_post_form = PostForm(request.POST, request.FILES, instance=current_post)
       if edit_post_form.is_valid():
           instance = edit_post_form.save(commit=False)
           instance.author=request.user
           instance.save() 
           messages.success(request, "Your Post is edited!")
           return redirect(reverse('posts-page'))
    else:
        edit_post_form = PostForm(instance=current_post) 
    return render(request, 'blog/edit_post.html', {"edit_post_form": edit_post_form})
