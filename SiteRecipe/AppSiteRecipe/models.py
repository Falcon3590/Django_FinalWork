from django.db import models
from django.contrib.auth.models import User


# Таблица рецептов. Один пользователь может создавать множество рецептов
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    cooking_steps = models.CharField(max_length=250)
    cooking_time = models.IntegerField(default=30)
    image = models.ImageField(upload_to='images/', null=True)
    author = models.CharField(max_length=100, null=True)

    def set_author(self, username):
        self.author = username

    def set_user(self, user):
        self.user = User.objects.get(id=user)

    def __str__(self):
        return f'{self.name}, {self.description}, время приготовления - {self.cooking_time} мин.'


# Таблица Категории рецептов
class RecipeCategories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Таблица Состав категории (показывает какие рецепты есть в категории)
class CategoryComposition(models.Model):
    id_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    id_recipe_category = models.ForeignKey(RecipeCategories, on_delete=models.CASCADE)

    def set_recipe(self):
        recipe = Recipe.objects.all().order_by('id').last()
        self.id_recipe = recipe