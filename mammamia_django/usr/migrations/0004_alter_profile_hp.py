# Generated by Django 4.0 on 2022-04-24 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0003_alter_profile_hp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hp',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]