# Generated by Django 4.0 on 2022-07-01 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_remove_product_bahan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('note', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
