# Generated by Django 4.1.6 on 2023-02-10 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
