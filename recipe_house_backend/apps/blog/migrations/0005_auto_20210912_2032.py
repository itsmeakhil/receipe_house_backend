# Generated by Django 3.0.4 on 2021-09-12 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210831_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='blog',
            name='type',
        ),
        migrations.DeleteModel(
            name='BlogType',
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ManyToManyField(blank=True, to='blog.Category'),
        ),
        migrations.AddField(
            model_name='blog',
            name='cuisine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Cuisine'),
        ),
    ]