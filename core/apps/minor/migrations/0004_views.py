# Generated by Django 5.0.6 on 2024-07-15 16:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minor', '0003_drugs'),
        ('singer', '0005_task_cnt_bm'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='views', to='singer.task', verbose_name='Задача')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='views', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Просмотры задачи',
                'verbose_name_plural': 'Просмотры задачей',
                'db_table': 'views',
            },
        ),
    ]
