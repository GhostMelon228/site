from django.db import models
from django.contrib.auth.models import User
from core.apps.singer.models import Task


class UserTaskEnroll(models.Model):
    user = models.ForeignKey(
        User,
        related_name="usertaskenroll",
        verbose_name="Автор",
        on_delete=models.PROTECT
    )
    task = models.ForeignKey(
        Task,
        related_name="usertaskenroll",
        verbose_name="Категория",
        on_delete=models.PROTECT
    )

    STATUS_CHOICES = [
        ('NA', '_'),
        ('PC', 'Решается'),
        ('WA', 'Неправильно'),
        ('OK', 'Правильно')
    ]
    status = models.CharField(
        verbose_name="Состояние задачи", max_length=15, choices=STATUS_CHOICES, default='NA', blank=True)
    

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"
        db_table = 'usertaskenroll'
        unique_together = ["user", "task"]

    def __str__(self):
        return f"Ответ {self.user} на {self.task}"

class UserAnswers(models.Model):
    user = models.ForeignKey(
        User,
        related_name="useranswers",
        verbose_name="Автор",
        on_delete=models.PROTECT
    )
    task = models.ForeignKey(
        Task,
        related_name="useranswers",
        verbose_name="Категория",
        on_delete=models.PROTECT
    )

    STATUS_CHOICES = [
        ('NA', '_'),
        ('PC', 'Решается'),
        ('WA', 'Неправильно'),
        ('OK', 'Правильно')
    ]
    status = models.CharField(
        verbose_name="Состояние задачи", max_length=15, choices=STATUS_CHOICES, default='NA', blank=True)
    

    class Meta:
        verbose_name = "Попытка пользователя"
        verbose_name_plural = "Попытки пользователей"
        db_table = 'useranswers'

    def __str__(self):
        return f"Попытка {self.user} на {self.task}"

class Drugs(models.Model):    #типо zakladki

    user = models.ForeignKey(
        User,
        related_name="savedtasks",
        verbose_name="Автор",
        on_delete=models.PROTECT
    )
    task = models.ForeignKey(
        Task,
        related_name="savedtasks",
        verbose_name="Категория",
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Отмечанная задача"
        verbose_name_plural = "Отмечанные задачи"
        db_table = 'savedtasks'
        unique_together = ["user", "task"]

    def __str__(self):
        return f"Z Задача {self.task} пользователя {self.user}"



class FavouriteTask(models.Model):       #типо likess

    user = models.ForeignKey(
        User,
        related_name="favouritetask",
        verbose_name="Автор",
        on_delete=models.PROTECT
    )
    task = models.ForeignKey(
        Task,
        related_name="favouritetask",
        verbose_name="Категория",
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Любимая задача"
        verbose_name_plural = "Любимые задачи"
        db_table = 'favouritetask'
        unique_together = ["user", "task"]

    def __str__(self):
        return f"O Задача {self.task} пользователя {self.user}"
