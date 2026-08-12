from django.urls import path
from . import views


urlpatterns = [
    path(route="", view=views.main_page, name="main_page"),
    path(route="register/", view=views.RegisterView.as_view(), name="registration"),
    path(route="login/", view=views.LoginView.as_view(), name="login"),
    path(route="logout/", view=views.LogoutView.as_view(), name="logout"),
    path(route="profile/", view=views.ProfileView.as_view(), name="profile"),
    path(route="profile/update/", view=views.ProfileUpdateView.as_view(), name="profile_update"),
    path(route="profile/change/", view=views.PasswordChangeView.as_view(), name="password_change"),
    
]