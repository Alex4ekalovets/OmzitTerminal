# Generated by Django 4.2.4 on 2023-10-02 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0023_rename_model_query_workshopschedule_model_order_query'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopschedule',
            name='workshop',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Цех'),
        ),
    ]
