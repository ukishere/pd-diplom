# Generated by Django 3.1.2 on 2020-10-30 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20201030_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='dt',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания'),
        ),
    ]
