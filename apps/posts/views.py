from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment
from . import forms



class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(
            request=request,
            template_name="posts/post_list.html",
            context={"posts":posts}
        )


class PostDetailView(View):
    def get(self, request, pk):
        form = forms.CommentForm(data=None)
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        return render(
            request=request,
            template_name="posts/post_detail.html",
            context={
                "post": post, 
                "form":form, 
                "comments":comments
                }
        )

    def post(self, request, pk):
        form = forms.CommentForm(data=request.POST)
        post = Post.objects.get(pk=pk)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect("post_detail", post.pk)

        return render(
                    request=request,
                    template_name="posts/post_detail.html",
                    context={"post": post, "form":form}
                )


class PostCreateView(View):
    def get(self, request):
        form = forms.PostCreateForm(data=None)
        return render(
            request=request,
            template_name="posts/post_create.html",
            context={"form":form}
        )


    def post(self, request):
        form = forms.PostCreateForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post.pk)

        return render(
                    request=request,
                    template_name="posts/post_create.html",
                    context={"form":form}
                )


class PostUpdateView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = forms.PostCreateForm(instance=post)
        return render(
            request=request,
            template_name="posts/post_update.html",
            context = {"form":form}
        )


    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = forms.PostCreateForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", post.pk)

        return render(
                    request=request,
                    template_name="posts/post_update.html",
                    context = {"form":form}
                )


class PostDeleteView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        return render(
            request=request,
            template_name="posts/post_delete.html",
            context={"post":post}
        )

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("post_list")