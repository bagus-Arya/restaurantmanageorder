# Generated by Django 4.0 on 2022-06-30 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0012_remove_pesanan_history_is_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storestatus',
            name='user_id',
        ),
    ]
