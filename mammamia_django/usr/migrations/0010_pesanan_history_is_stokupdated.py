# Generated by Django 4.0 on 2022-05-08 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0009_alter_detail_pesanan_history_date_detail_pesanan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesanan_history',
            name='is_stokUpdated',
            field=models.IntegerField(default='0'),
        ),
    ]