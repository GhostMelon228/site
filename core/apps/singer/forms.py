from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import (
    FieldDoesNotExist,
    ImproperlyConfigured,
    ValidationError,
)

from core.apps.singer.models import Category, Task

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
            required=False,
            widget=forms.PasswordInput(
                    attrs={
                        'class': 'form-control', 'placeholder': 'Введите пароль'
                    }
            )
    )
    password2 = forms.CharField(
            required=False,
            widget=forms.PasswordInput(
                    attrs={
                        'class': 'form-control', 'placeholder': 'Подтвердите пароль'
                    }
            )
    )

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email',)
        widgets = {
            'username': forms.TextInput(
                    attrs=({
                        'class': 'form-control',
                        'placeholder': 'Ник',
                    })
            ),
            'last_name': forms.TextInput(
                    attrs=({
                        'class': 'form-control',
                        'placeholder': 'Фамилия',
                    })
            ),
            'first_name': forms.TextInput(
                    attrs=({
                        'class': 'form-control',
                        'placeholder': 'Имя'
                    })
            ),
            'email': forms.TextInput(
                    attrs=({
                        'class': 'form-control',
                        'placeholder': 'example.com'
                    })
            ),
        }
    

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        self.fields['email'].widget.attrs.update(autofocus=False)

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if username and self._meta.model.objects.filter(username__iexact=username).exists():
            return self.add_error("username", "Ай ай ай, нарушитель!!")
        
        return username   

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")

        if first_name == "":
            return self.add_error("first_name", "Ай ай ай, нарушитель!!")
        
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        if last_name == "":
            return self.add_error("last_name", "Ай ай ай, нарушитель!!")
        
        return last_name
    

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(email)

        if email == '':
            return self.add_error("email", "Ай ай ай, нарушитель!!")
        
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 or not password2:
            self.add_error('password2', 'Введите пароль!')
            return self.add_error('password1', 'Введите пароль')
        elif password1 != password2:
            self.add_error('password2', 'Пароли не совпадают!')
            return self.add_error('password1', 'Пароли не совпадают!')

        return password2
    

    def _post_clean(self):
        super(forms.BaseModelForm, self)._post_clean()
        password = self.cleaned_data.get("password2")
        if password:
            try:
                print(self.instance, 'jkgjhmgjf')
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                for e in error:
                    print(e, type(e))
                    if e == 'This password is too short. It must contain at least 8 characters.':
                        self.add_error("password1", 'Пароль слишком короткий (минимум 8 символов).')
                    if e == 'This password is too common.':
                        self.add_error("password1", 'Пароль, ну, слишком популярный.')
                    if e == 'This password is entirely numeric.':
                        self.add_error("password1", 'Пароль, состоящий только из цифр, не оч')
                print(error, type(error))
                #self.add_error("password2", error)

    def is_valid(self) -> bool:

        errors = self.errors.as_data()
        print(errors)
        for field in self.fields:
            if field not in errors:
                class_ = "form-control is-valid"
            else:
                class_ = "form-control is-invalid"
            self.fields[field].widget.attrs.update(
                {'class': class_}
            )

        if errors and ('password1' in self.fields or 'password2' in self.fields):
            self.fields['password1'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.fields['password2'].widget.attrs.update({'class': 'form-control is-invalid'})

        return super().is_valid()

class UserLoginForm(AuthenticationForm):
    def is_valid(self):
        
        errors = self.errors.as_data()
        for field in self.fields:
            if field not in errors:
                class_ = "form-control is-valid"
            else:
                class_ = "form-control is-invalid"
            self.fields[field].widget.attrs.update(
                {'class': class_}
            )
        return super().is_valid()



class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("description", "answer", "category",)

        widgets = {
            "description":forms.Textarea(
                attrs=({'class': 'form-control', 'rows':'5'})
            ),
            "answer":forms.TextInput(
                attrs=({'class':'form-control'})
            ),
            "category":forms.Select(
                attrs=({'class':'form-select'})
            ),
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
    

    
    def clean_description(self):
        description = self.cleaned_data.get("description")

        if description == "":
            return self.add_error("description", "Ай ай ай, нарушитель!!")
        
        return description

    def clean_answer(self):
        answer = self.cleaned_data.get("answer")

        if answer == "":
            return self.add_error("answer", "Ай ай ай, нарушитель!!")
        
        return answer
    

    def clean_category(self):
        category = self.cleaned_data.get("category")
        print(category)

        if category == None or category == "---------":
            return self.add_error("category", "Ай ай ай, нарушитель!!")
        
        return category
    


    def is_valid(self) -> bool:

        errors = self.errors.as_data()

        for field in self.fields:

            if field not in errors:
                class_ = "form-control is-valid"
            else:
                class_ = "form-control is-invalid"
            
            self.fields[field].widget.attrs.update(
                {'class': class_}
            )

        
        return super().is_valid()



class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("title",)

        widgets = {
            "title":forms.Textarea(
                attrs=({'class': 'form-control', 'rows': '1'})
            ),
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    
    def clean_title(self):
        title = self.cleaned_data.get("title")

        if title == "":
            return self.add_error("title", "Ай ай ай, нарушитель!!")
        elif title[0].isdigit():
            return self.add_error("title", "nарушитель!!")
        
        return title
    


    def is_valid(self) -> bool:

        errors = self.errors.as_data()

        for field in self.fields:
            
            if field not in errors:
                class_ = "form-control is-valid"
            else:
                class_ = "form-control is-invalid"
            
            self.fields[field].widget.attrs.update(
                {'class': class_}
            )

        
        return super().is_valid()