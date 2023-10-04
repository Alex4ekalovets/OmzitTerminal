# Generated by Django 4.2.4 on 2023-10-03 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0028_alter_shifttask_datetime_done_alter_shifttask_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shifttask',
            name='datetime_create',
        ),
        migrations.RemoveField(
            model_name='shifttask',
            name='datetime_update',
        ),
        migrations.AlterField(
            model_name='shifttask',
            name='datetime_techdata_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата/время занесения технологических данных'),
        ),
        migrations.AlterField(
            model_name='shifttask',
            name='datetime_techdata_update',
            field=models.DateTimeField(auto_now=True, verbose_name='дата/время корректировки технологических данных'),
        ),
    ]
