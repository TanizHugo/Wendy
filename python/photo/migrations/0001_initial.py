# Generated by Django 3.2.16 on 2023-03-26 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='唯一编号')),
                ('use', models.CharField(max_length=64, verbose_name='用途')),
                ('path', models.CharField(max_length=64, verbose_name='图片路径')),
            ],
            options={
                'db_table': 'pic',
            },
        ),
    ]
