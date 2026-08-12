from django.urls import path
from . import views

urlpatterns = [
    path(route="", view=views.PostListView.as_view(), name="post_list"),
    path(route="<int:pk>/", view=views.PostDetailView.as_view(), name="post_detail"),
    path(route="create/", view=views.PostCreateView.as_view(), name="post_create"),
    path(route="<int:pk>/update/", view=views.PostUpdateView.as_view(), name="post_update"),
    path(route="<int:pk>/delete/", view=views.PostDeleteView.as_view(), name="post_delete"),
    path(route="comment/<int:pk>/update/", view=views.CommentUpdateView.as_view(), name="comment_update"),
    path(route="comment/<int:pk>/delete/", view=views.CommentDeleteView.as_view(), name="comment_delete")
]