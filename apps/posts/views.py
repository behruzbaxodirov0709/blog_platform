from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q



class PostListView(View):
    def get(self, request):
        query = request.GET.get("q")
        posts = Post.objects.annotate(comments_count = Count("comments"))
        if query:
            posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
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
        post.views_count += 1
        post.save()
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
        if not request.user.is_authenticated:
            return redirect("login")
        
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


class PostCreateView(LoginRequiredMixin, View):
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
        if post.author == request.user:    
            form = forms.PostCreateForm(instance=post)
            return render(
                request=request,
                template_name="posts/post_update.html",
                context = {"form":form}
            )

        else:
            return redirect("main_page")




    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.author == request.user:
            form = forms.PostCreateForm(data=request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect("post_detail", post.pk)

            return render(
                        request=request,
                        template_name="posts/post_update.html",
                        context = {"form":form}
                    )

        else:
            return redirect("main_page")


class PostDeleteView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.author == request.user:
            return render(
                request=request,
                template_name="posts/post_delete.html",
                context={"post":post}
            )

        else:
            return redirect("main_page")

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.author == request.user:
            post.delete()
            return redirect("post_list")
        else:
            return redirect("main_page")


class CommentUpdateView(View):
    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.author == request.user:
            form = forms.CommentForm(data=None, instance=comment)
            return render(
                request=request,
                template_name="posts/comment_update.html",
                context={"form":form, "comment":comment}
            )

        else:
            return redirect("main_page")

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.author == request.user:
            form = forms.CommentForm(data=request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect("post_detail", comment.post.pk)

            return render(
                request=request,
                template_name="posts/comment_update.html",
                context={"form":form, "comment":comment}
                )

        else:
            return redirect("main_page")


class CommentDeleteView(View):
    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.author == request.user:
            return render(
                request=request,
                template_name="posts/comment_delete.html",
                context={"comment":comment}
            )

        else:
            return redirect("main_page")

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.author == request.user:
            post_pk = comment.post.pk
            comment.delete()
            return redirect("post_detail", post_pk)

        else:
            return redirect("main_page")