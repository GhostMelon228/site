from django.contrib import admin

from core.apps.minor.models import UserTaskEnroll, UserAnswers, FavouriteTask, Drugs


@admin.register(UserTaskEnroll)
class UserTaskEnrollAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'task', 'status',)

@admin.register(UserAnswers)
class UserAnswersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'task', 'status',)

@admin.register(Drugs)
class DrugsTaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'task',)

@admin.register(FavouriteTask)
class FavouriteTaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'task',)
