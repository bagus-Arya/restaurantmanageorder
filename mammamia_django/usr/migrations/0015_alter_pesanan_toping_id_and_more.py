# Generated by Django 4.0 on 2022-07-02 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0014_pesanan_note_customer_pesanan_toping_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesanan',
            name='toping_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pesanan_history',
            name='toping_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]