# Generated by Django 3.2 on 2022-02-16 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favourites', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favouritepost',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]