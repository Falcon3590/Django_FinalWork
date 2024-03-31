from .models import Recipe, RecipeCategories, CategoryComposition
from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, PasswordInput, ValidationError
from django import forms


class UserRegistrationForm(ModelForm):
    password = CharField(label='Пароль', widget=PasswordInput)
    password2 = CharField(label='Пароль повторно', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {'username': 'Имя пользователя',
                  'email': 'Почта'}

    # вызывается в момент проверки формы в файле views
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class NewRecipe(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'description', 'cooking_steps', 'cooking_time')  # , 'image')
        labels = {'name': 'Название',
                  'description': 'Описание блюда',
                  'cooking_steps': 'Шаги приготовления',
                  'cooking_time': 'Время приготовления'}
        # 'image': 'Изображение'}


class CategoryCompositionForm(ModelForm):
    class Meta:
        model = CategoryComposition
        fields = ('id_recipe_category',)
        labels = {'id_recipe_category': 'Категория рецепта'}
