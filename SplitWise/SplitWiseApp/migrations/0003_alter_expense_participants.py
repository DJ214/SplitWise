# Generated by Django 3.2.9 on 2024-02-11 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SplitWiseApp', '0002_auto_20240211_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='participants',
            field=models.ManyToManyField(to='SplitWiseApp.User'),
        ),
    ]