from django.contrib import admin

from core.apps.singer.models import Task, Category

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'answer', 'category', 'cnt_likes', 'cnt_views', 'cnt_bm',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',)

admin.register(Task, TaskAdmin)
admin.register(Category, CategoryAdmin)