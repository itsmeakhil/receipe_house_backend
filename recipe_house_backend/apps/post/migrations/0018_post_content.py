# Generated by Django 3.0.4 on 2022-01-22 10:34

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0017_auto_20220122_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(default='a'),
            preserve_default=False,
        ),
    ]