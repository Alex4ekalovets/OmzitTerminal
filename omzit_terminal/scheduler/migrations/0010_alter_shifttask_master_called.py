# Generated by Django 4.2.4 on 2023-08-30 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0009_shifttask_master_called_alter_shifttask_master_calls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shifttask',
            name='master_called',
            field=models.CharField(default='не было', null=True),
        ),
    ]
