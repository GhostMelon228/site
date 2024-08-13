from django.contrib import admin
from django.urls import path

from core.apps.singer.views import index, index2, index3, index4, index5, index6_1, index6_2, add_category, add_task,watch_likes
from core.apps.singer.views import UserRegistrationView, TaskListViews, TaskDetailView, TaskCreateView, CategoryCreateView, FavouriteTaskListViews, DrugsListViews, LikesListViews, HistoryListViews, SeenTaskListViews, CategoryListViews

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='UserRegistration'),

    path('tasks/', TaskListViews.as_view()),
    path('tasks/add_task', TaskCreateView.as_view(), name='add_task'),
    path('categories/add_category', CategoryCreateView.as_view(), name='add_category'),

    path('tasks/<int:task_id>/', TaskDetailView.as_view()),
    path('categories/<int:category_id>', CategoryListViews.as_view()),
    path('views/', SeenTaskListViews.as_view()),
    path('history/', HistoryListViews.as_view()),

    path('likes', FavouriteTaskListViews.as_view()),
    path('likes/add/<int:task_id>', TaskDetailView.create_like),
    path('likes/del/<int:task_id>', TaskDetailView.delete_like),
    path('likes/watch', LikesListViews.as_view()),

    path('bm/', DrugsListViews.as_view()),
    path('bm/add/<int:task_id>', TaskDetailView.create_bm),
    path('bm/del/<int:task_id>', TaskDetailView.delete_bm),
]