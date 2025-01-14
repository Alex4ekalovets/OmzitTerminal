# Generated by Django 4.2.4 on 2024-01-19 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tehnolog', '0006_alter_techdata_draw_filename_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pip',
            fields=[
                ('wo_number', models.CharField(db_column='WONumber', max_length=50, primary_key=True, serialize=False)),
                ('part_name', models.CharField(db_column='PartName', max_length=100)),
                ('program_name', models.CharField(db_column='ProgramName', max_length=50)),
                ('repeat_id', models.IntegerField(db_column='RepeatID')),
                ('qty_in_process', models.IntegerField(blank=True, db_column='QtyInProcess', null=True)),
                ('cutting_time', models.FloatField(blank=True, db_column='CuttingTime', null=True)),
                ('cutting_length', models.FloatField(blank=True, db_column='CuttingLength', null=True)),
                ('pierce_qty', models.IntegerField(blank=True, db_column='PierceQty', null=True)),
                ('total_cutting_time', models.FloatField(blank=True, db_column='TotalCuttingTime', null=True)),
                ('master_part_qty', models.IntegerField(blank=True, db_column='MasterPartQty', null=True)),
                ('wo_state', models.IntegerField(blank=True, db_column='WOState', null=True)),
                ('pk_pip', models.CharField(db_column='PK_PIP', max_length=36)),
            ],
            options={
                'db_table': 'pip',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('program_name', models.CharField(db_column='ProgramName', max_length=50, primary_key=True, serialize=False)),
                ('repeat_id', models.IntegerField(db_column='RepeatID')),
                ('qty_in_process', models.IntegerField(blank=True, db_column='QtyInProcess', null=True)),
                ('cutting_time', models.FloatField(blank=True, db_column='CuttingTime', null=True)),
                ('pierce_qty', models.IntegerField(blank=True, db_column='PierceQty', null=True)),
                ('post_datetime', models.DateTimeField(blank=True, db_column='PostDateTime', null=True)),
                ('material', models.CharField(blank=True, db_column='Material', max_length=150, null=True)),
                ('thickness', models.FloatField(blank=True, db_column='Thickness', null=True)),
                ('posted_by_user_id', models.IntegerField(blank=True, db_column='PostedByUserID', null=True)),
                ('pk_program', models.CharField(db_column='PK_PROGRAM', max_length=36)),
            ],
            options={
                'db_table': 'program',
                'managed': False,
            },
        ),
    ]
