# Generated by Django 4.2.4 on 2023-10-03 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0031_alter_shifttask_model_order_query_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shifttask',
            name='excel_list_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Лист excel технологического процесса'),
        ),
    ]
