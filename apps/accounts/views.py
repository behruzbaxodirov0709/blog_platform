from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django import forms



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



            
            

