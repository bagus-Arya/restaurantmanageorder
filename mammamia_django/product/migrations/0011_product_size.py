# Generated by Django 4.0 on 2022-07-01 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_topping'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
