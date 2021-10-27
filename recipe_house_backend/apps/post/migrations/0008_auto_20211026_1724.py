# Generated by Django 3.0.4 on 2021-10-26 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20211018_1048'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='CATEGORY_name_d8768d_idx'),
        ),
        migrations.AddIndex(
            model_name='cuisine',
            index=models.Index(fields=['name'], name='CUISINE_name_9f564b_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['title'], name='POST_title_b9de8e_idx'),
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='TAG_name_264c46_idx'),
        ),
    ]