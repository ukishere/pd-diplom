# Generated by Django 3.1.2 on 2020-10-30 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20201030_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='dt',
            field=models.DateTimeField(verbose_name='Дата и время создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='for_whom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='for_whom', to='orders.forwhom', verbose_name='Куда доставляем'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
