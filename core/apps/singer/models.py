from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
#from core.apps.minor.models import UserTaskEnrollwelcometoeurobambam


class Category(models.Model):
    title = models.TextField(
        verbose_name="Название", max_length=30
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = 'category'
    
    def __str__(self):
        return f"Категория {self.pk}"
    def get_absolute_url(self):
        return reverse("add_category")
    

class Task(models.Model):
    description = models.TextField(
        verbose_name="Условие задачи", max_length=1000, blank=True
    )
    answer = models.TextField(
        verbose_name="Ответ", max_length=1000,
    )
    author = models.ForeignKey(
        User,
        related_name="tasks",
        verbose_name="Автор",
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        Category,
        related_name="tasks",
        verbose_name="Категория",
        on_delete=models.PROTECT
    )
    cnt_likes = models.IntegerField(
        verbose_name="Кол-во лайков",
        max_length=None, default=0
    )
    cnt_views = models.IntegerField(
        verbose_name="Просмотры",
        default=0
    )
    cnt_bm = models.IntegerField(
        verbose_name="Кол-во zakladki",
        max_length=None, default=0
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        db_table = 'tasks'

    def __str__(self):
        return f"Задача № {self.pk}"
    
    def get_absolute_url(self):
        return reverse("add_task")
