# from django.shortcuts import render
#
# # Create your views here.
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Post, Comment
# from .forms import PostForm, CommentForm
#
# from django.core.paginator import Paginator
# from django.shortcuts import render
# from .models import Post
#
# def post_list(request):
#     posts = Post.objects.all().order_by('-date_posted')
#     paginator = Paginator(posts, 5)  # Show 5 posts per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'blog/post_list.html', {'posts': page_obj})
#
#
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     comments = post.comments.all()
#
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('post-detail', pk=post.pk)
#     else:
#         form = CommentForm()
#
#     return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})
#
# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)  # Handle file uploads
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post_list')
#     else:
#         form = PostForm()
#     return render(request, 'blog/create_post.html', {'form': form})
#
# def like_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#     comment.likes += 1
#     comment.save()
#     return redirect('post_detail', pk=comment.post.pk)
#
#
# from django.shortcuts import get_object_or_404, reverse
# from django.http import HttpResponseRedirect
# from .models import Post
#
# def like_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     # Like or unlike the post
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)  # Unlike the post
#     else:
#         post.likes.add(request.user)  # Like the post
#
#     # Redirect back to post detail page
#     return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
#
#
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Post, Comment
# from .forms import CommentForm
#
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     comments = post.comments.all()  # Retrieve all comments related to the post
#     comment_form = CommentForm()
#
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.post = post  # Attach the post to the comment
#             comment.author = request.user  # Attach the current logged-in user
#             comment.save()
#             return redirect('post-detail', pk=pk)
#
#     context = {
#         'post': post,
#         'comment_form': comment_form,
#         'comments': comments,
#     }
#     return render(request, 'blog/post_detail.html', context)
#
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Comment, Reply
from .forms import PostForm, CommentForm, ReplyForm

from django.core.paginator import Paginator


# List all posts with pagination
def post_list(request):
    posts = Post.objects.all().order_by('-date_posted')
    paginator = Paginator(posts, 5)  # Show 5 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'posts': page_obj})


# Post detail view: displays post details, comments, and handles new comments and replies
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()  # Retrieve all comments related to the post
    comment_form = CommentForm()
    reply_form = ReplyForm()

    if request.method == 'POST':
        # Handle comment form submission
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post  # Attach the post to the comment
                comment.author = request.user  # Attach the current logged-in user
                comment.save()
                return redirect('post-detail', pk=pk)

        # Handle reply form submission
        elif 'reply_form' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                comment_id = request.POST.get('comment_id')
                comment = get_object_or_404(Comment, id=comment_id)
                reply = reply_form.save(commit=False)
                reply.comment = comment  # Attach the reply to the comment
                reply.author = request.user  # Attach the current logged-in user
                reply.save()
                return redirect('post-detail', pk=pk)

    context = {
        'post': post,
        'comment_form': comment_form,
        'reply_form': reply_form,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)


# Create a new post
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


# Like or unlike a post
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Like or unlike the post
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)  # Unlike the post
    else:
        post.likes.add(request.user)  # Like the post

    # Redirect back to post detail page
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


# Like or unlike a comment
from django.shortcuts import get_object_or_404, redirect
from .models import Comment


def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Toggle like/unlike for the comment
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)  # Unlike the comment
    else:
        comment.likes.add(request.user)  # Like the comment

    # Redirect back to the post detail page
    return redirect('post-detail', pk=comment.post.pk)


# Reply to a comment
def reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.comment = comment  # Attach the reply to the comment
            reply.author = request.user  # Attach the current logged-in user
            reply.save()
            return redirect('post-detail', pk=comment.post.pk)

    context = {
        'comment': comment,
        'reply_form': reply_form,
    }
    return render(request, 'blog/post_detail.html', context)
