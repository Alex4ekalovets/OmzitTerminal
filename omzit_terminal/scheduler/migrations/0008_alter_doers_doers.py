# Generated by Django 4.2.4 on 2023-08-28 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0007_doers_alter_shifttask_fio_doer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doers',
            name='doers',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
