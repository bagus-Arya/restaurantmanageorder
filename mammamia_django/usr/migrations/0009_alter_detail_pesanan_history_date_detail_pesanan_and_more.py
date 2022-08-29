# Generated by Django 4.0 on 2022-05-07 03:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0008_alter_detail_pesanan_history_date_detail_pesanan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail_pesanan_history',
            name='date_detail_pesanan',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pesanan',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pesanan_history',
            name='date_added_history',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]