# Generated by Django 4.0 on 2022-05-04 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0006_remove_pesanan_history_is_history_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesanan_history',
            name='is_history',
            field=models.IntegerField(default='0'),
        ),
    ]
