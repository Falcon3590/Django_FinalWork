from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserRegistrationForm, LoginForm, NewRecipe, CategoryCompositionForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Recipe


# Create your views here.
def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        # Проверка формы (сравнение двух паролей)
        if user_form.is_valid():
            # Создаем пользователя, но пока не сохраняем в бд. Сохраняем в переменную new_user
            new_user = user_form.save(commit=False)
            # Устанавливаем пароль для пользователя, хешируем пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в БД
            new_user.save()
            return redirect('/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        # Создание экземпляра формы
        form = LoginForm(request.POST)
        if form.is_valid():  # проверка валидности формы
            cd = form.cleaned_data
            # поиск пользователей в бд с помощью метода authenticate
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user = User.objects.filter(username=cd['username'])[0].id
                    return redirect(f'/user/{user}/')
                else:
                    return HttpResponse('Отключенная учетная запись')
            else:
                return HttpResponse('Неверный логин или пароль')
    else:
        # Создание новой формы авторизации
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def main(request, id_user):
    if request.method == 'POST':
        try:
            recipe_form = NewRecipe(request.POST)
        except:
            return HttpResponse('Произошла ошибка при создании рецепта')
        if recipe_form.is_valid():
            # Создаем рецепт, но пока не сохраняем в бд. Сохраняем в переменную new_recipe
            new_recipe = recipe_form.save(commit=False)
            # Устанавливаем
            new_recipe.set_user(id_user)
            author = User.objects.get(id=id_user).username
            new_recipe.set_author(author)
            # Сохраняем в БД
            new_recipe.save()
            # Создаем форму для выбора категории
            form = CategoryCompositionForm()
            return render(request, 'recipe_new.html', {'recipe_form': form})
        try:
            category_composition_form = CategoryCompositionForm(request.POST)
        except:
            return HttpResponse('Произошла ошибка при выборе категории')
        if category_composition_form.is_valid():  # Проверяем отправлена ли форма с категорией
            category_composition = category_composition_form.save(commit=False)
            category_composition.set_recipe()
            category_composition.save()
            return render(request, 'base.html')
    return render(request, 'base.html')


def new_recipe(request, id_user):
    recipe_form = NewRecipe()
    return render(request, 'recipe_new.html', {'recipe_form': recipe_form})


def new_update(request, id_user):
    answer = Recipe.objects.filter(user_id=id_user)
    list_a = []
    for i in answer:
        list_a.append([f'update/{i.id}/', i])
    return render(request, 'update.html', {'list_a': list_a})


def update_recipe(request, id_user, id_recipe):
    try:
        old_data = get_object_or_404(Recipe, id=id_recipe)
    except:
        return HttpResponse('Такой товар не существует')
    if request.method == 'POST':
        form = NewRecipe(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/user/{id_user}/')
    else:
        form = NewRecipe(instance=old_data)
        return render(request, 'update_recipe.html', context={'form': form})


def recipe(request):
    all_resipe = Recipe.objects.all()
    if len(all_resipe) > 5:
        answer = Recipe.objects.order_by('?')[:5]
    else:
        answer = all_resipe
    list_a = []
    for i in answer:
        list_a.append([f'info/{i.id}/', i])
    return render(request, 'recipe.html', {'list_a': list_a})


def info_recipe(request, id_recipe):
    recipe = Recipe.objects.get(id=id_recipe)
    context = {'name': recipe.name,
               'description': recipe.description,
               'cooking_steps': recipe.cooking_steps,
               'cooking_time': recipe.cooking_time,
               'author': recipe.author}
    return render(request, 'info_recipe.html', context=context)
