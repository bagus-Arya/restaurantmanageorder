# Generated by Django 4.0 on 2022-04-29 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0004_alter_profile_hp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesanan_history',
            name='quantity_history',
            field=models.IntegerField(default='0'),
        ),
    ]