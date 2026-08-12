from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm, LoginForm, ProfileUpdateForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin



@login_required
def main_page(request):
    return render(request=request, template_name="main_page.html")




class RegisterView(View):
    def get(self, request):
        form = SignUpForm(data=None)
        return render(
            request=request,
            template_name="accounts/register.html",
            context={"form":form}
        )

    def post(self, request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()

            return redirect("main_page")

        return render(
                    request=request,
                    template_name="accounts/register.html",
                    context={"form":form}
                )


class LoginView(View):
    def get(self, request):
        form = LoginForm(data=None)
        return render(
            request=request,
            template_name="accounts/login.html",
            context={"form":form}
        )

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user is None:
                form.add_error(field="password", error="Username yoki parol xato")
                return render(
                            request=request,
                            template_name="accounts/login.html",
                            context={"form":form}
                        )

            login(request=request, user=user)
            return redirect("main_page")


class LogoutView(View):
    def post(self, request):
        logout(request=request)
        return redirect("login")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request=request,
            template_name="accounts/profile.html",
            context={"user":request.user}
        )


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm(data=None, instance=request.user)
        return render(
            request=request,
            template_name="accounts/profile_update.html",
            context={"form":form}
        )

    def post(self, request):
        form = ProfileUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")

        return render(
                    request=request,
                    template_name="accounts/profile_update.html",
                    context={"form":form}
                )


class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(data=None, user=request.user)
        return render(
            request=request,
            template_name="accounts/password_change.html",
            context={"form":form}
        )

    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            request.user.set_password(new_password)
            request.user.save()
            return redirect("login")

        return render(
                    request=request,
                    template_name="accounts/password_change.html",
                    context={"form":form}
                )




        

