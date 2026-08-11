from django import forms
from .models import CustomUser


class SignUpForm(forms.ModelForm):
    confirmation_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Parolni takrorlang'
        }
    ))
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "phone_number", "address", "password"]
        widgets = {
            "password":forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Parolni kiriting...'
                }
            )
        }    


    def clean(self):
        data = super().clean()
        password = data.get("password")
        confirmation_password = data.get("confirmation_password")
        username = data.get("username")


        if password and confirmation_password and password != confirmation_password:
            raise forms.ValidationError("Parollar mos emas")

        if password and username and password.lower() == username.lower():
            raise forms.ValidationError("Username va password bir xil bo'lmasligi lozim!")

        return data


    def clean_password(self):
        password = self.cleaned_data["password"]


        if len(password)<8:
            raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lsin")

        if password[0].isdigit():
            raise forms.ValidationError("Parol son bilan boshlanmasligi lozim!")



        letters = []
        for x in password:
            if x.isalpha():
                letters.append(x)

        if len(letters)<3:
            raise forms.ValidationError("Parolda kamida 3 ta harfdan iborat bo'lishi lozim!")



        numbers = []
        for number in password:
            if number.isdigit():
                numbers.append(number)

        if len(numbers)<5:
            raise forms.ValidationError("Parolda kamida 5 ta raqamdan iborat bo'lishi lozim")



        lower_letters = []
        upper_letters = []
        for letter in letters:
            if letter.isupper():
                upper_letters.append(letter)

            elif letter.islower():
                lower_letters.append(letter)

        if len(upper_letters)<1:
            raise forms.ValidationError("Parolda kamida 1 ta katta harf qatnashishi lozim!")

        if len(lower_letters)<2:
            raise forms.ValidationError("Parolda kamida 2 ta kichkina harf qatnashishi lozim!")


        return password


    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username)<8:
            raise forms.ValidationError("Username kamida 8 ta belgidan iborat bo'lishi kerak!")



        numbers = []
        for number in username:
            if number.isdigit():
                numbers.append(number)

        if len(numbers)<3:
            raise forms.ValidationError("Usernameda kamida 3 ta raqam bo'lishi lozim!")



        letters = []
        for x in username:
            if x.isalpha():
                letters.append(x)

        if len(letters)<5:
            raise forms.ValidationError("Usernameda kamida 5 ta harfdan iborat bo'lishi lozim!")
        

        return username
        


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Usernamingizni kiriting...'
    }))
    password =forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parolingizni kiriting...'
    }))

